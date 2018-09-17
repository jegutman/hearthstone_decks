import sys
sys.path.append('../')
from config import basedir
sys.path.append(basedir)
sys.path.append(basedir + '/lineupSolver')
#from backports import csv
from datetime import datetime
from hearthstone.deckstrings import Deck
from hearthstone.deckstrings import FormatType
from label_archetype import label_archetype
import json
import os
import re
import requests
from pprint import pprint
import pycookiecheat
from fake_useragent import UserAgent
from deck_manager import *
#from conquest_utils import *
from lhs_utils import *

#### use Elo
from rate_hs_elo import *


ua = UserAgent()

deckstring_re = re.compile('(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{4}){12,}')

def calc_tiebreak(player, player_matches, max_round = 99999):
    #match = (game_time, bracket_name, round_num, p1, p2, result, p1_score, p2_score, games)
    opp_wins, opp_matches = 0, 0
    opps = []
    opp_wr = []
    opp_det = []
    round_num_opp = {}
    for game_time, bracket_name, round_num, p1, p2, result, p1_score, p2_score, games in player_matches[player]:
        if bracket_name != 'Swiss': continue
        #if -1 in [p1_score, p2_score]: continue
        if round_num > max_round: continue
        if p1 == player:
            opps.append(p2)
            round_num_opp[p2] = round_num
        else:
            opps.append(p1)
            round_num_opp[p1] = round_num
    for opp in opps:
        tmp_wins, tmp_matches = 0,0
        for game_time, bracket_name, round_num, p1, p2, result, p1_score, p2_score, games in sorted(player_matches[opp], key=lambda x:x[2]):
            if bracket_name != 'Swiss': continue
            if round_num > max_round: continue
            #if -1 in [p1_score, p2_score]: continue
            opp_matches += 1
            tmp_matches += 1
            if p1 == opp:
                if p1_score == -1: continue
                if result:
                    opp_wins += 1
                    tmp_wins += 1
            else:
                if p2_score == -1: continue
                if not result:
                    opp_wins += 1
                    tmp_wins += 1
        #print(opp, tmp_wins, tmp_matches)
        opp_wr.append(max(float(tmp_wins) / float(max(tmp_matches, 1)), 0.3))
        opp_det.append((round_num_opp[opp], opp, tmp_wins, tmp_matches))
    #print(opps, opp_wins, opp_matches, float(opp_wins) / opp_matches)
    cumm_wr = float(opp_wins) / opp_matches
    avg_wr = sum(opp_wr) / len(opp_wr)
    #tb_diff = round(avg_wr - cumm_wr, 4) * 100
    #return (round(avg_wr, 4), sorted(opp_det))
    return round(avg_wr, 4)
    

def search(x, y):
    for i,j in x.items():
        if y in str(j):
            print(i)

smashgg_hero_map = {
    617 : 'Paladin',
    618 : 'Druid',
    619 : 'Hunter',
    620 : 'Mage',
    621 : 'Priest',
    622 : 'Rogue',
    623 : 'Shaman',
    624 : 'Warlock',
    625 : 'Warrior',
}

def decks_from_smashgg_api(event_id, entrants, entrant_name_to_id):
    deck_api_url = 'https://api.smash.gg/cardDeck/deckString/%(event_id)s'
    data = json.loads(requests.get(deck_api_url % locals()).text)
    res = {}
    for long_name, deck_dict in data.items():
        if not deck_dict: continue
        decks = list(deck_dict.values())
        if long_name not in entrant_name_to_id:
            continue
        entrant_id = entrant_name_to_id[long_name]
        name = entrants[entrant_id]
        res[name] = decks
    return res

def parse_set_new(set_info, entrants, bracket_name):
    #set_url = 'https://api.smash.gg/set/%(match_id)s'
    #set_data = json.loads(requests.get(set_url % locals()).text)
    #set_info = set_data['entities']['sets']
    print("parsing %s" % set_info['id'])
    games = []
    round_number = set_info['round']
    game_time = set_info['updatedAt']
    p1_id = set_info['entrant1Id']
    p2_id = set_info['entrant2Id']
    if not p1_id or not p2_id:
        return []
    p1 = entrants[p1_id]
    p2 = entrants[p2_id]
    p1_classes = []
    p2_classes = []
    p1_score = set_info['entrant1Score']
    p2_score = set_info['entrant2Score']
    if p1_score is not None:
        p1_score = int(p1_score)
    if p2_score is not None:
        p2_score = int(p2_score)

    if p1_score is not None and p2_score is not None:
        result = 1 if p1_score > p2_score else 0
    else:
        result = -1
    match_res = [game_time, bracket_name, round_number, p1, p2, result, p1_score, p2_score]
    try:
    #if True:
        for game in set_info['games']:
            #p1_class = smashgg_hero_map[game['selections'][p1_id]['character'][0]['selectionValue']]
            #p2_class = smashgg_hero_map[game['selections'][p2_id]['character'][0]['selectionValue']]
            #game_result = 1 if game['winnerId'] == p1_id else 0
            #games.append((p1_class, p2_class, game_result))
            for pid in game['selections'].keys():
                if pid == str(p1_id):
                    p1_classes.append(smashgg_hero_map[game['selections'][pid]['character'][0]['selectionValue']])
                elif pid == str(p2_id):
                    p2_classes.append(smashgg_hero_map[game['selections'][pid]['character'][0]['selectionValue']])
            game_result = 1 if str(game['winnerId']) == str(p1_id) else 0
            games.append((p1_classes[-1], p2_classes[-1], game_result))
        match_res.append(games)
        #print(match_res)
    except:
        pass
    if len(match_res) == 8:
        match_res.append([])
    return match_res

def parse_set(match_id, entrants, bracket_name):
    print("parsing %s" % match_id)
    set_url = 'https://api.smash.gg/set/%(match_id)s'
    set_data = json.loads(requests.get(set_url % locals()).text)
    set_info = set_data['entities']['sets']
    games = []
    round_number = set_info['round']
    game_time = set_info['updatedAt']
    p1_id = set_info['entrant1Id']
    p2_id = set_info['entrant2Id']
    if not p1_id or not p2_id:
        return []
    p1 = entrants[p1_id]
    p2 = entrants[p2_id]
    p1_classes = []
    p2_classes = []
    p1_score = set_info['entrant1Score']
    p2_score = set_info['entrant2Score']
    if p1_score is not None:
        p1_score = int(p1_score)
    if p2_score is not None:
        p2_score = int(p2_score)

    if p1_score is not None and p2_score is not None:
        result = 1 if p1_score > p2_score else 0
    else:
        result = -1
    match_res = [game_time, bracket_name, round_number, p1, p2, result, p1_score, p2_score]
    try:
    #if True:
        for game in set_info['games']:
            #p1_class = smashgg_hero_map[game['selections'][p1_id]['character'][0]['selectionValue']]
            #p2_class = smashgg_hero_map[game['selections'][p2_id]['character'][0]['selectionValue']]
            #game_result = 1 if game['winnerId'] == p1_id else 0
            #games.append((p1_class, p2_class, game_result))
            for pid in game['selections'].keys():
                if pid == str(p1_id):
                    p1_classes.append(smashgg_hero_map[game['selections'][pid]['character'][0]['selectionValue']])
                elif pid == str(p2_id):
                    p2_classes.append(smashgg_hero_map[game['selections'][pid]['character'][0]['selectionValue']])
            game_result = 1 if str(game['winnerId']) == str(p1_id) else 0
            games.append((p1_classes[-1], p2_classes[-1], game_result))
        match_res.append(games)
        #print(match_res)
    except:
        pass
    if len(match_res) == 8:
        match_res.append([])
    return match_res


#### API Tournament
#### 'https://api.smash.gg/tournament/dreamhack-hct-grand-prix-tours-2018?expand[]=phase&expand[]=groups&expand[]=event

data = None
bracket_data = None
def parse_smash_tournament(tournament_name):
    global data, bracket_data
    decks = {}
    matches = []
    tournament_url = 'https://api.smash.gg/tournament/%(tournament_name)s?expand[]=phase&expand[]=groups&expand[]=event'
    #bracket_url = 'https://api.smash.gg/phase_group/%(bracket_id)s?expand[]=entrants&expand[]=sets'
    bracket_url = 'https://api.smash.gg/phase_group/%(bracket_id)s?expand[]=entrants&expand[]=seeds&expand[]=sets'
    # TODO: use https://api.smash.gg/phase_group/589463?expand%5B%5D=entrants&expand%5B%5D=seeds&expand%5B%5D=sets for games
    tournament_data = json.loads(requests.get(tournament_url % locals()).text)
    data = tournament_data
    event_id = data['entities']['event'][0]['id']
    print(event_id)
    phase_map = {}
    player_matches = {}
    url_slug = 'https://smash.gg/' + tournament_data['entities']['event'][0]['slug'].replace('event', 'events') + '/brackets/%(phase_id)s'
    for phase_data in tournament_data['entities']['phase']:
        phase_map[phase_data['id']] = phase_data['name']
    for bracket in tournament_data['entities']['groups']:
        entrants = {}
        entrant_name_to_id = {}
        bracket_id = bracket['id']
        phase_id = bracket['phaseId']
        print(phase_id)
        bracket_name = phase_map[bracket['phaseId']]
        print(bracket_url % locals())
        bracket_data = json.loads(requests.get(bracket_url % locals()).text)
        try:
            for entrant_data in bracket_data['entities']['entrants']:
                entrants[entrant_data['id']] = tuple(entrant_data['mutations']['players'].values())[0]['gamerTag'].split('#')[0].strip()
                entrant_name_to_id[entrant_data['name']] = entrant_data['id']
        except:
            print("bracket failed")
            continue
        #decks.update(decks_from_smashgg(url_slug % locals(), entrants))
        decks.update(decks_from_smashgg_api(event_id, entrants, entrant_name_to_id))
        #for i in sorted(entrants.values()):
        #    print(i)
        max_ids = len(bracket_data['entities']['sets'])
        id_count = 0
        for set_data in bracket_data['entities']['sets']:
            id_count +=1
            match_id = set_data['id']
            #p1_id = set_data['entrant1Id']
            #p2_id = set_data['entrant2Id']
            #if not p1_id or not p2_id: continue
            #p1 = entrants[p1_id]
            #p2 = entrants[p2_id]
            #p1_score = int(set_data['entrant1Score']) if set_data['entrant1Score'] else 0
            #p2_score = int(set_data['entrant2Score']) if set_data['entrant2Score'] else 0
            #result = 1 if p1_score > p2_score else 0
            #game_time = set_data['completedAt']
            ##game_time = datetime.fromtimestamp(set_data['completedAt'])
            ##date = game_time.strftime("%Y_%m_%d %H:%M:%S")
            #round_num = set_data['round']
            #games = []
            #match_res = (game_time, bracket_name, round_num, p1, p2, result, p1_score, p2_score, games)
            #player_matches[p1] = player_matches.get(p1, []) + [match_res]
            #player_matches[p2] = player_matches.get(p2, []) + [match_res]
            #matches.append(match_res)
            ##print(match_res)
            #match_res = parse_set(match_id, entrants, bracket_name)
            match_res = parse_set_new(set_data, entrants, bracket_name)
            if match_res:
                p1, p2 = match_res[3], match_res[4]
                print(id_count,max_ids,'  ', end='')
                player_matches[p1] = player_matches.get(p1, []) + [match_res]
                player_matches[p2] = player_matches.get(p2, []) + [match_res]
                matches.append(match_res)

    return decks, matches, player_matches

def get_stats(decks, matches, player_matches, player_filter=None):
    #match_res = [game_time, bracket_name, round_number, p1, p2, result, p1_score, p2_score, games]
    wins = {}
    losses = {}
    archetypes = {}
    class_archetypes = {}
    for x in player_matches.keys():
        losses[x] = sum([1-i[5] if i[3] == x else i[5] for i in player_matches[x]])
        wins[x] = sum([i[5] if i[3] == x else 1-i[5] for i in player_matches[x]])
    for player, lineup in sorted(decks.items(), key=lambda x:wins.get(x[0], 0)):
        archetypes[player] = []
        class_archetypes[player] = {}
        for deck in lineup:
            try:
                tmp = EasyDeck(deck)
            except:
                print('bad deck: %s %s' % (player, deck))
                label = label_archetype(tmp)
            if label:
                archetypes[player].append(label)
                class_archetypes[player][label.split(' ')[-1]] = label
        archetypes[player] = sorted(archetypes[player], key=lambda x:x.split(' ')[1])
    matchups = {}
    a_games = {}
    a_wins = {}
    for game_time, bracket_name, round_number, p1, p2, result, p1_score, p2_score, games in sorted(matches, key=lambda x:x[2]):
        #if wins.get(p1, 0) < 4 or wins.get(p2, 0) < 4:
        #    continue
        for c1, c2, res in games:
            a1 = class_archetypes[p1].get(c1)
            a2 = class_archetypes[p2].get(c2)
            print(p1, p2, round_number, a1, a2, res)
            if a1 and a2:
                #print(p1, p2, a1, a2)
                if a1 != a2:
                    a_games[(a1, a2)] = a_games.get((a1, a2), 0) + 1
                    a_games[(a2, a1)] = a_games.get((a2, a1), 0) + 1
                    a_games[a1] = a_games.get(a1, 0) + 1
                    a_games[a2] = a_games.get(a2, 0) + 1
                    if res == 1:
                        a_wins[(a1, a2)] = a_wins.get((a1, a2), 0) + 1
                        a_wins[a1] = a_wins.get(a1, 0) + 1
                    else:
                        a_wins[(a2, a1)] = a_wins.get((a2, a1), 0) + 1
                        a_wins[a2] = a_wins.get(a2, 0) + 1
    return a_games, a_wins

def print_stats(a_games, a_wins):
    for i, j in sorted(a_games.items(), key=lambda x:x[1], reverse=True):
        if len(i) == 2 and i[0] < i[1]:
            print("%-20s %-20s %s-%s" % (i[0], i[1],a_wins.get(i,0),j-a_wins.get(i,0)))

def get_player_archetype(lineups, player, card_class):
    tmp = [c for c in lineups[player] if card_class in c]

if __name__ == '__main__':
    #decks = decks_from_smashgg('https://smash.gg/tournament/dreamhack-hct-grand-prix-tours-2018/event/dreamhack-hct-hearthstone-grand-prix-tours-2018/brackets/239288')
    #decks, matches = parse_smash_tournament('dreamhack-hct-grand-prix-tours-2018')
    #decks = decks_from_smashgg('https://smash.gg/tournament/dreamhack-hct-grand-prix-tours-2018/event/dreamhack-hct-hearthstone-grand-prix-tours-2018')
    #decks = decks_from_smashgg('https://smash.gg/tournament/dreamhack-hct-grand-prix-tours-2018/events/dreamhack-hct-hearthstone-grand-prix-tours-2018/brackets/239288')
    #decks = decks_from_smashgg('https://smash.gg/tournament/dreamhack-hct-grand-prix-tours-2018/event/dreamhack-hct-hearthstone-grand-prix-tours-2018/brackets/239288')

    #decks, matches, player_matches = parse_smash_tournament('dreamhack-hct-grand-prix-austin-2018')
    decks, matches, player_matches = parse_smash_tournament('dreamhack-hct-grand-prix-montreal-2018-1')
    #decks, matches, player_matches = parse_smash_tournament('dreamhack-hct-grand-prix-summer-2018')
    #decks, matches, player_matches = parse_smash_tournament('hct-toronto-at-eglx-2018-1')
    wins = {}
    losses = {}
    archetypes = {}
    class_archetypes = {}
    for x in player_matches.keys():
        total_losses = sum([1-i[5] if i[3] == x else i[5] for i in player_matches[x]])
        total_wins = sum([i[5] if i[3] == x else 1-i[5] for i in player_matches[x]])
        wins[x] = total_wins
        losses[x] = total_losses

    for player, lineup in sorted(decks.items(), key=lambda x:wins.get(x[0], 0)):
        archetypes[player] = []
        class_archetypes[player] = {}
        for deck in lineup:
            try:
                tmp = EasyDeck(deck)
            except:
                print('bad deck: %s %s' % (player, deck))
                continue
            label = label_archetype(tmp)
            if label:
                archetypes[player].append(label)
                class_archetypes[player][label.split(' ')[-1]] = label
            else:
                print(player)
                print(deck)
                tmp.print_deck()
        archetypes[player] = sorted(archetypes[player], key=lambda x:x.split(' ')[1])
        #if wins.get(player, 0) >= 7:
        #    print(",".join(sorted(archetypes[player], key=lambda x:x.split(' ')[1])))
    for i,j in archetypes.items():
        if len(j) >0 and len(j) != 4:
            if i in wins: 
                print(wins[i], i, j)

    from json_win_rates import *
    win_pcts, num_games, game_count, wr_archetypes, overall_wr = get_win_pcts(min_game_threshold=0, min_game_count=0,limitTop=100)
    RNGs = ['Insom', 'Kolmari', 'ETC', 'Jengo']
    def print_ogs(matches, round_filter = 1,show_wr=True, OGs=None, bracket_filter = None):
        global win_pcts
        if OGs == None:
            OGs = ['Level9001', 'Ginky', 'TheChosenGuy', 'SwaggyG', 'Villain', 'Caravaggio', 'Ryder', 'seohyun628', 'XisBau5e', 'Qwerty97', 'Luker', 'Fenom', 'kuonet', 'Guiyze', 'killinallday', 'zlsjs', 'lnguagehackr']
        round_wins = {}
        to_print = []
        for date, bracket, round_num, p1, p2, result, score1, score2,  games in sorted(matches, key=lambda x:x[2]):
            if round_num < round_filter:
                if result:
                    round_wins[p1] = round_wins.get(p1, 0) + 1
                else:
                    round_wins[p2] = round_wins.get(p2, 0) + 1
            if (p1 in OGs or p2 in OGs) and int(round_num) >= round_filter:
                if bracket_filter and bracket != bracket_filter: continue
                if p2 in OGs and p1 not in OGs:
                    p1, p2 = p2, p1
                    score1, score2 = score2, score1
                l1, l2 = archetypes[p1], archetypes[p2]
                if not score1: score1 = 0
                if not score2: score2 = 0
                if len(l1) == 4 and len(l2) == 4 and show_wr:
                    #wr = win_rate(archetypes[p1], archetypes[p2], win_pcts)[1]
                    try:
                        wr = pre_ban_nash_calc(archetypes[p1], archetypes[p2], win_pcts)
                        wr = "%5.3f" % wr
                    except:
                        wr = "NaN"
                else:
                    wr = 'Could not calculate'
                #ws = wins.get(p1, 0)
                #ls = losses.get(p1, 0)
                #print("%s %-20s %-20s %s %s %s %s %s" % (round_num, p1, p2, score1, score2, wr, ws, ls))
                score_summ = "%s - %s" % (round_wins.get(p1, 0), round_filter - 1 - round_wins.get(p1, 0))
                score_summ2 = "%s - %s" % (round_wins.get(p2, 0), round_filter - 1 - round_wins.get(p2, 0))
                #print("%s %-20s %-20s %s %s %s   %s" % (round_num, p1, p2, score1, score2, wr, score_summ))
                to_print.append((round_wins.get(p1, 0), "%s %-20s %-20s %s %s %s   %s | %s" % (round_num, p1, p2, score1, score2, wr, score_summ, score_summ2)))
                #to_print.append((round_wins.get(p1, 0), "%s %-20s %-20s %s %s %s   %s %s %s" % (round_num, p1, p2, score1, score2, wr, score_summ, calc_tiebreak(p1, player_matches), calc_tiebreak(p2,  player_matches))))
        for i, j in sorted(to_print, reverse=True):
            print(j)
    
    count = 0
    #print("\n\nFIELD")
    #for player, score in sorted(wins.items(), key=lambda x:(x[1], calc_tiebreak(x[0], player_matches)), reverse=True):
    #    if score >= 0:
    #        #count += 1
    #        #print("%2s %-15s %s %s" % (count, player, score, calc_tiebreak(player, player_matches)))
    #        print('"' + ",".join(archetypes[player]) + '", #' + player)

    #a_games, a_wins = get_stats(decks, matches, player_matches)
    #print_stats(a_games, a_wins)

    def expect_score_local(r1, r2):
        rating_diff = r2 - r1
        return 1 / (1 + 10 ** (rating_diff / 1135.77))

    print_ogs(matches, round_filter = 1,show_wr=True, OGs=None, bracket_filter = None)
    #print_ogs(matches, round_filter = 1,show_wr=True, OGs=['zlsjs'], bracket_filter = None)
    print('\n')
    #print_ogs(matches, round_filter = 1,show_wr=True, OGs=RNGs, bracket_filter = None)
    def print_lu(a, b):
        print('"' + ",".join(archetypes[a]) + '"',  '"' + ",".join(archetypes[b]) + '"')

