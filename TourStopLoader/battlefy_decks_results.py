import sys
sys.path.append('../')
from config import basedir
sys.path.append(basedir)
sys.path.append(basedir + '/lineupSolver')
#from backports import csv
from hearthstone.deckstrings import Deck
import json
from deck_manager import *
import re
import requests
from label_archetype import label_archetype
from conquest_utils import calculate_win_rate
from json_win_rates import *

win_pcts, num_games, game_count, archetypes, overall_wr = get_win_pcts(min_game_threshold=0, min_game_count=0,limitTop=100)

deckstring_re = re.compile('(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{4}){12,}')

def print_player(player):
    for i in player_matches[player]:
        if i[2] == player:
            print(i[2], i[3], i[5], i[6])
            for j in i[-1]:
                print('    ',j)
        else:
            print(i[3], i[2], i[6], i[5])
            for j in i[-1]:
                j = (j[1], j[0], 1-j[2])
                print('    ',j)

def parse_deck(text):
    for i in range(3):
        try:
            deck = Deck.from_deckstring(text+'='*i)
            return deck
        except Exception as e:
            continue
    return None

player_decks = {}
seeds = {}

def matches_from_battlefy(battlefy_url, code_dest=None):
    valid = re.compile(r"^(?:https://)?\/?battlefy.com\/([^:/\s]+)/([^:\/\s]+)/([\w\d]+)/stage/([\w\d]+)/bracket/(\d*)$")
    bracketf= 'https://dtmwra1jsgyb0.cloudfront.net/stages/{}/matches'
    matchf = 'https://dtmwra1jsgyb0.cloudfront.net/matches/{}?extend%5Btop.team%5D%5Bplayers%5D%5Buser%5D=true&extend%5Bbottom.team%5D%5Bplayers%5D%5Buser%5D=true'
    matches = valid.match(battlefy_url)
    if matches is None:
        print("Unable to parse battlefy url. Please get the bracket from the brackets tab")
        return
    groups = matches.groups()
    org = groups[0]
    event = groups[1]
    stagecode = groups[3]
    bracket_url = bracketf.format(stagecode)
    data = json.loads(requests.get(bracket_url).text)

    return data

"""
NOTES ON battlefy parsing
get names game['top']['team']['name']
get deck codes game['top']['customFields']  (mabye [-4:])
'bannedClass'
'winner'
games in  game['stats']
    ['top']['class']
    ['top']['winner']
"""
def parse_match(match):
    global player_decks, seeds
    matchf = 'https://dtmwra1jsgyb0.cloudfront.net/matches/{}?extend%5Btop.team%5D%5Bplayers%5D%5Buser%5D=true&extend%5Bbottom.team%5D%5Bplayers%5D%5Buser%5D=true'
    if 'isComplete' not in match.keys():
        return None
    elif match['isBye']:
        return None
    if not match['top'] or not match['bottom']:
        return None
    if 'team' not in match['top']:
        return None
    if 'team' not in match['bottom']:
        return None
    date = match['updatedAt'][:10].replace('-', '_')
    round_number = match['roundNumber']
    p1 = match['top']['team']['name'].replace(' \#', '#').split(' ')[0].split('(')[0]
    p1 = p1.split('#')[0]
    if p1 not in player_decks: player_decks[p1] = []
    p2 = match['bottom']['team']['name'].replace(' #', '#').split(' ')[0].split('(')[0]
    p2 = p2.split('#')[0]
    if p2 not in player_decks: player_decks[p2] = []

    if 'seedNumber' in match['top']:
        seeds[p1] = match['top']['seedNumber']
    if 'seedNumber' in match['bottom']:
        seeds[p2] = match['bottom']['seedNumber']

    p1_decks = player_decks.get(p1, [])
    p2_decks = player_decks.get(p2, [])
    if not p1_decks or not p2_decks:
        try:
            if not p1_decks:
                for field in match['top']['team']['customFields']:
                    deck_match = deckstring_re.findall(field['value'])
                    if deck_match:
                        p1_decks.append(deck_match[0])
                player_decks[p1] = p1_decks
            if not p2_decks:
                for field in match['bottom']['team']['customFields']:
                    deck_match = deckstring_re.findall(field['value'])
                    if deck_match:
                        p2_decks.append(deck_match[0])
                player_decks[p2] = p2_decks
        except:
            r = requests.get(matchf.format(match['_id']))
            matchdata = json.loads(r.text)
            if not p1_decks:
                team = matchdata[0]['top']
                if 'team' in team:
                    try:
                        decks = team['team']['players'][0]['gameAttributes']['deckStrings']
                        for decklist in decks:
                            deck = parse_deck(decklist)
                            if deck!=None:
                                p1_decks.append(deck.as_deckstring)
                    except:
                        pass
                player_decks[p1] = p1_decks
            if not p2_decks:
                team = matchdata[0]['bottom']
                if 'team' in team:
                    try:
                        decks = team['team']['players'][0]['gameAttributes']['deckStrings']
                        for decklist in decks:
                            deck = parse_deck(decklist)
                            if deck!=None:
                                p2_decks.append(deck.as_deckstring)
                    except:
                        pass
                player_decks[p2] = p2_decks

    if 'bannedClass' in match['top']:
        p1_banned = match['top']['bannedClass']
    else:
        p1_banned = ''
    if 'bannedClass' in match['bottom']:
        p2_banned = match['bottom']['bannedClass']
    else:
        p2_banned = ''
    

    result = 1 if match['top']['winner'] else 0
    
    games = []
    if 'stats' in match.keys():
        for game in match['stats']:
            p1_tmp_class = game['stats']['top']['class']
            p2_tmp_class = game['stats']['bottom']['class']
            tmp_result = 1 if game['stats']['top']['winner'] else 0
            games.append((p1_tmp_class, p2_tmp_class, tmp_result))

    p1_score = match['top']['score']
    p2_score = match['bottom']['score']
    
    return (date, round_number, p1, p2, result, p1_score, p2_score, games)

def get_decks(match):
    p1_decks = []
    p2_decks = []
    matchf = 'https://dtmwra1jsgyb0.cloudfront.net/matches/{}?extend%5Btop.team%5D%5Bplayers%5D%5Buser%5D=true&extend%5Bbottom.team%5D%5Bplayers%5D%5Buser%5D=true'
    if 'isComplete' not in match.keys():
        return None
    elif match['isBye']:
        return None
    if not match['top'] or not match['bottom']:
        return None
    if 'team' not in match['top']:
        return None
    if 'team' not in match['bottom']:
        return None
    try:
        for field in match['top']['team']['customFields']:
            deck_match = deckstring_re.findall(field['value'])
            if deck_match:
                p1_decks.append(deck_match[0])
        for field in match['bottom']['team']['customFields']:
            deck_match = deckstring_re.findall(field['value'])
            if deck_match:
                p2_decks.append(deck_match[0])
    except:
        r = requests.get(matchf.format(match['_id']))
        matchdata = json.loads(r.text)
        team = matchdata[0]['top']
        if 'team' in team:
            try:
                decks = team['team']['players'][0]['gameAttributes']['deckStrings']
                for decklist in decks:
                    deck = parse_deck(decklist)
                    if deck!=None:
                        p1_decks.append(deck.as_deckstring)
            except:
                pass
        team = matchdata[0]['bottom']
        if 'team' in team:
            try:
                decks = team['team']['players'][0]['gameAttributes']['deckStrings']
                for decklist in decks:
                    deck = parse_deck(decklist)
                    if deck!=None:
                        p2_decks.append(deck.as_deckstring)
            except:
                pass
    return p1_decks, p2_decks
        
def process_battlefy_url(bracket_url):
    matches = []
    failed = []
    count = 0
    player_matches = {}

    #for bracket_url in bracket_urls:

    data = matches_from_battlefy(bracket_url)
    decks = {}

    for match_data in data:
        count += 1
        match = parse_match(match_data)
        if not match:
            failed.append(match_data)
        else:
            matches.append(match)
            p1, p2 = match[2], match[3]
            p1 = p1.split('#')[0].strip()
            p2 = p2.split('#')[0].strip()
            player_matches[p1] = player_matches.get(p1, []) + [match]
            player_matches[p2] = player_matches.get(p2, []) + [match]
            if p1 not in decks or p2 not in decks:
                p1_decks, p2_decks = get_decks(match_data)
                decks[p1] = p1_decks
                decks[p2] = p2_decks
                
    return decks, matches, player_matches
            
        #try:
        #    p1 = i['top']['team']['name']
        #    p2 = i['bottom']['team']['name']
        #    try:
        #        seeds[i['top']['seedNumber']] = p1
        #        seeds[i['bottom']['seedNumber']] = p2
        #    except:
        #        pass
        #    result = 'W' if i['top']['winner'] else 'L'
        #except:
        #    failed.append(i)
        #    continue
        #matches.append((p1,p2,result))
    #wins = {}
    #losses = {}
    #for x in player_matches.keys():
    #    total_losses = sum([1-i[4] if i[2] == x else i[4] for i in player_matches[x]])
    #    total_wins = sum([i[4] if i[2] == x else 1-i[4] for i in player_matches[x]])
    #    wins[x] = total_wins
    #    losses[x] = total_losses
    #    if total_losses == 0 and total_wins >5:
    #        print(x)

if __name__ == '__main__':
    urls = [
        #'https://battlefy.com/take-tv/hct-germany-a-taketv-tour-stop-european-qualifier-3/5b3511182c185e0397195e61/stage/5b4c500dee3d0303d602e337/bracket/',
        #'https://battlefy.com/take-tv/hct-germany-a-taketv-tour-stop-european-qualifier-3/5b3511182c185e0397195e61/stage/5b4c5032bd99a703aa907fb7/bracket/',
        #'https://battlefy.com/take-tv/hct-germany-a-taketv-tour-stop-european-qualifier-3/5b3511182c185e0397195e61/stage/5b4c501fbd99a703aa907eb6/bracket/',
        #'https://battlefy.com/take-tv/hct-germany-a-taketv-tour-stop-european-qualifier-3/5b3511182c185e0397195e61/stage/5b4c503d4f4bb503a14b2352/bracket/',
        #'https://battlefy.com/evox/hct-tour-stop-italy-powered-by-zotac/5aa7d09f0b25e50393914521/stage/5aa7d0ba0f99cf034ea52f06/bracket/',
        #'https://battlefy.com/hearthstone-global-games-2018/hearthstone-global-games-2018/5b3ccaa722962f03ce590019/stage/5b3ccb149a4af103b49c2aa6/bracket/1',
    ]
    player_matches = {}
    decks = {}
    archetypes = {}
    all_matches = []
    for url in urls:
        tmp_decks, tmp_matches, tmp_player_matches = process_battlefy_url(url)
        # this is not quite right because could be lists to append to
        player_matches.update(tmp_player_matches)
        decks.update(tmp_decks)
        all_matches += tmp_matches

    wins = {}
    losses = {}
    for x in player_matches.keys():
        total_losses = sum([1-i[4] if i[2] == x else i[4] for i in player_matches[x]])
        total_wins = sum([i[4] if i[2] == x else 1-i[4] for i in player_matches[x]])
        wins[x] = total_wins
        losses[x] = total_losses

    for player, lineup in decks.items():
        archetypes[player] = []
        for deck in lineup:
            tmp = EasyDeck(deck)
            label = label_archetype(tmp)
            if label:
                archetypes[player].append(label)
        if wins[player] >= 7:
            print(",".join(sorted(archetypes[player], key=lambda x:x.split(' ')[1])))

    for i,j in archetypes.items():
        if len(j) >0 and len(j) != 4:
            if i in wins: 
                print(losses.get(i, 0), wins[i], i, j)
    #for date, round_number, p1, p2, result, p1_score, p2_score, games in all_matches:
    #    p1_lineup = archetypes[p1]
    #    p2_lineup = archetypes[p2]
    #    if len(p1_lineup) == 4 and len(p2_lineup) == 4:
    #        print(",".join([str(i) for i in [p1, p2, calculate_win_rate(p1_lineup, p2_lineup, win_pcts), p1_score, p2_score]]))

    #for date, round_number, p1, p2, result, p1_score, p2_score, games in all_matches:
    #    p1_lineup = archetypes[p1]
    #    p2_lineup = archetypes[p2]
    #    if len(p1_lineup) == 4 and len(p2_lineup) == 4:
    #        wr = calculate_win_rate(p1_lineup, p2_lineup, win_pcts)
    #        if wr > 0.65 or wr < 0.35 and wr != 0 and wr != 1:
    #            res = 'W' if p1_score > p2_score else 'L'
    #            upset = ''
    #            if res == 'W' and wr < 0.5: upset = 'UPSET'
    #            if res == 'L' and wr > 0.5: upset = 'UPSET'
    #            print(",".join([str(i) for i in [p1, p2, wr, res, upset]]))
