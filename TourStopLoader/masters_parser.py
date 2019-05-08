#parsing tournament
# 1) Check if tournament is finished (maybe just stage) or loaded
# 2) Parse each stage
# 3) load tournament info into db
# 4) Parse each match
# 5) Check if decks have been loaded
# 6) If they haven't load the lineup for the player and create player_id for tournament
# 7) 

import sys
sys.path.append('../')
from config import basedir
sys.path.append(basedir)
sys.path.append(basedir + '/lineupSolver')
from pprint import pprint
import json, requests
import datetime
import pytz
from dateutil import parser
from deck_manager import EasyDeck
from label_archetype_file import label_archetype
import os
import re
os.environ['TZ'] = 'America/Chicago'

#deckstring_re = re.compile('AA(?:[A-Za-z0-9+/]{2})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{4}){12,}')
deckstring_re = re.compile('AA[A-Za-z0-9+/]+=*')

all_cups_url = 'https://playhearthstone.com/en-us/esports/schedule/scheduleData?month=%(month)s&year=%(year)s'
tournament_info_url = 'https://dtmwra1jsgyb0.cloudfront.net/tournaments/%(tournament_id)s'
all_matches_url = 'https://dtmwra1jsgyb0.cloudfront.net/stages/%(stage_id)s/matches'
match_info_url = 'https://dtmwra1jsgyb0.cloudfront.net/matches/%(match_id)s?extend%%5Btop.team%%5D%%5Bplayers%%5D%%5Buser%%5D=true&extend%%5Bbottom.team%%5D%%5Bplayers%%5D%%5Buser%%5D=true'
stage_link_str = 'https://battlefy.com/hsesports/hearthstone-masters-qualifiers/%(tournament_id)s/stage/%(stage_id)s/bracket/'
alt_tournament_info_url = 'https://majestic.battlefy.com/hearthstone-masters/tournaments?start=%(start_date)s&end=%(end_date)s'
tournament_link_str = 'https://battlefy.com/hsesports/%(tournament_name)s/%(tournament_id)s/'
archetypes = {}

def get_time_from_utc(timestr):
    utc_time = parser.parse(timestr)
    local_tz = pytz.timezone('America/Chicago')
    local_time = utc_time.replace(tzinfo=datetime.timezone.utc).astimezone(tz=local_tz)
    return int(local_time.strftime("%s"))

def get_masters_cups(end_date):
    # returns list of (id, date, region, name)
    res = []
    start_date = '2019-03-01'
    tournaments = json.loads(requests.get(alt_tournament_info_url % locals()).text)
    for tourn in tournaments:
        #utc_time = parser.parse(tourn['startTime'])
        #local_time = utc_time.replace(tzinfo=datetime.timezone.utc).astimezone(tz=None)
        #etime = int(local_time.strftime("%s"))
        etime = get_time_from_utc(tourn['startTime'])
        res.append((tourn['_id'], etime, tourn['region'], tourn['slug']))
    return res

def get_stage_ids(tournament_id):
    data_tourney = json.loads(requests.get(tournament_info_url % locals()).text)
    stage_ids = data_tourney['stageIDs']
    return stage_ids

def get_stage_link(tournament_id, stage_id):
    return stage_link_str % locals()

def get_stage_games(stage_id):
    return json.loads(requests.get(all_matches_url % locals()).text)

def check_legal(lineup):
    if len(lineup) < 3: return True
    try:
        decks = [EasyDeck(i) for i in lineup]
    except:
        return True
    if decks[0].get_distance(decks[1]) > 5:
        return False
    if decks[0].get_distance(decks[2]) > 5:
        return False
    return True

#def get_matches(tournament_id, stage_id):

player_tourn_decks = {}
player_tourn_names = {}
player_ids = {}
player_games = {}
player_wins = {}
player_match_wins = {}
player_matches = {}
player_events = {}
def get_match_info(tournament_id, match):
    match_id = match['_id']
    p1_id = match['top']['team']['captainID']
    p2_id = match['bottom']['team']['captainID']
    p1_score = match['top']['score']
    p2_score = match['bottom']['score']
    #pprint(match)
    round_num = match['roundNumber']
    winner = match['top']['team']['name'] if match['top']['winner'] else match['bottom']['team']['name']
    if (tournament_id, p1_id) not in player_tourn_decks:
        match_info = json.loads(requests.get(match_info_url % locals()).text)
        p1_name = match_info[0]['top']['team']['players'][0]['inGameName']
        if tournament_id not in player_ids:
            player_ids[tournament_id] = {}
        player_ids[tournament_id][p1_name] = p1_id
        p1_decks = []
        if 'deckStrings' in match_info[0]['top']['team']['players'][0]['gameAttributes']:
            for i in match_info[0]['top']['team']['players'][0]['gameAttributes']['deckStrings']:
                p1_decks.append(deckstring_re.findall(i)[0])
        player_tourn_decks[(tournament_id, p1_id)] = p1_decks
        player_tourn_names[(tournament_id, p1_id)] = p1_name
        if not check_legal(p1_decks):
            print("ILLEGAL LINEUP", p1_name, " ".join(p1_decks))
    else:
        p1_name = player_tourn_names[(tournament_id, p1_id)]
        p1_decks = player_tourn_decks[(tournament_id, p1_id)]
    if (tournament_id, p2_id) not in player_tourn_decks:
        p2_name = match_info[0]['bottom']['team']['players'][0]['inGameName']
        player_ids[tournament_id][p2_name] = p2_id
        p2_decks = []
        if 'deckStrings' in match_info[0]['bottom']['team']['players'][0]['gameAttributes']:
            for i in match_info[0]['bottom']['team']['players'][0]['gameAttributes']['deckStrings']:
                p2_decks.append(deckstring_re.findall(i)[0])
            player_tourn_decks[(tournament_id, p2_id)] = p2_decks
        player_tourn_names[(tournament_id, p2_id)] = p2_name
        if not check_legal(p2_decks):
            print("ILLEGAL LINEUP", p2_name, " ".join(p2_decks))
    else:
        p2_name = player_tourn_names[(tournament_id, p2_id)]
        p2_decks = player_tourn_decks[(tournament_id, p2_id)]
    if p1_name == winner:
        player_match_wins[p1_name] = player_match_wins.get(p1_name, 0) + 1
    else:
        player_match_wins[p2_name] = player_match_wins.get(p2_name, 0) + 1
    player_games[p1_name] = player_games.get(p1_name, 0) + p1_score + p2_score
    player_games[p2_name] = player_games.get(p2_name, 0) + p1_score + p2_score
    player_wins[p1_name] = player_wins.get(p1_name, 0) + p1_score
    player_wins[p2_name] = player_wins.get(p2_name, 0) + p2_score
    if p1_name not in player_events:
        player_events[p1_name] = set()
    if p2_name not in player_events:
        player_events[p2_name] = set()
    player_events[p1_name].add(tournament_id)
    player_events[p2_name].add(tournament_id)
    player_matches[p1_name] = player_matches.get(p1_name, 0) + 1
    player_matches[p2_name] = player_matches.get(p2_name, 0) + 1
    if p1_decks:
        a1 = label_archetype(p1_decks[0])
        archetypes[a1] = archetypes.get(a1, 0) + 1
    if p2_decks:
        a2 = label_archetype(p2_decks[0])
        archetypes[a2] = archetypes.get(a2, 0) + 1
    #print(round_num, p1_name, p2_name, p1_score, p2_score, winner, label_archetype(p1_decks[0]) if p1_decks else None, label_archetype(p2_decks[0]) if p2_decks else None)
    

month, year = 3, 2019
start_date = '2019-03-01'
end_date = '2024-12-31'
cups_data = json.loads(requests.get(all_cups_url % locals()).text)

for tournament_id, tournament_time, tournament_region, tournament_name in get_masters_cups(end_date):
    #print("x")
    date_str = datetime.datetime.fromtimestamp(tournament_time).strftime("%Y_%m_%d %H:%M")
    #tournament_id = tourn['eventLink'].split('/')[-2]
    stage_ids = get_stage_ids(tournament_id)
    # HERE IS WHERE WE WOULD GET ALL OF THE GAMES
    #for stage_id in stage_ids:
    #    all_matches = json.loads(requests.get(all_matches_url % locals()).text)
    #    print(len(all_matches))
    if len(stage_ids) < 2: 
        print("%s,%s,%s" % (tournament_name.split('-')[-1], date_str, tournament_link_str % locals()))
        continue
    swiss_link = get_stage_link(tournament_id, stage_ids[0])
    swiss_games = get_stage_games(stage_ids[0])
    for game in swiss_games:
        if not game['isBye']:
            get_match_info(tournament_id, game)
    top8_link = get_stage_link(tournament_id, stage_ids[1])
    top8_games = get_stage_games(stage_ids[-1])
    if 'completedAt' not in top8_games[-1]: continue
    for game in top8_games:
        get_match_info(tournament_id, game)
    match_id = top8_games[-1]['_id']
    finals = json.loads(requests.get(match_info_url % locals()).text)
    finals_name = finals[0]['top']['team']['name']
    winner = finals[0]['top']['team']['name'] if finals[0]['top']['winner'] else finals[0]['bottom']['team']['name']
    print("\n%s,%s,%s,%s,%s,%s\n" % (tournament_name.split('-')[-1], date_str, tournament_link_str % locals(), swiss_link, top8_link, winner))
    tmp_final = top8_games[-1]


if True:
    for i,j in sorted(player_wins.items(), key=lambda x:x[1], reverse=True)[:50]:
        print("%-20s %s %s  %s %%" % (i,j, player_games[i], int(100 * j / player_games[i])))

for i,j in sorted(archetypes.itesm(), key=lambda x:x[1], reverse=True):
    print("%-25s %s" % (i,j))
