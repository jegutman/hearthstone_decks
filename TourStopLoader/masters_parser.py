#parsing tournament
# 1) Check if tournament is finished (maybe just stage) or loaded
# 2) Parse each stage
# 3) load tournament info into db
# 4) Parse each match
# 5) Check if decks have been loaded
# 6) If they haven't load the lineup for the player and create player_id for tournament
# 7) 

import json, requests
import datetime
from dateutil import parser

all_cups_url = 'https://playhearthstone.com/en-us/esports/schedule/scheduleData?month=%(month)s&year=%(year)s'
tournament_info_url = 'https://dtmwra1jsgyb0.cloudfront.net/tournaments/%(tournament_id)s'
all_matches_url = 'https://dtmwra1jsgyb0.cloudfront.net/stages/%(stage_id)s/matches'
match_info_url = 'https://dtmwra1jsgyb0.cloudfront.net/matches/%(match_id)s?extend%%5Btop.team%%5D%%5Bplayers%%5D%%5Buser%%5D=true&extend%%5Bbottom.team%%5D%%5Bplayers%%5D%%5Buser%%5D=true'
stage_link_str = 'https://battlefy.com/hsesports/hearthstone-masters-qualifiers-las-vegas-1/%(tournament_id)s/stage/%(stage_id)s/bracket/'
alt_tournament_info_url = 'https://majestic.battlefy.com/hearthstone-masters/tournaments?start=%(start_date)s&end=%(end_date)s'
tournament_link_str = 'https://battlefy.com/hsesports/%(tournament_name)s/%(tournament_id)s/'

def get_time_from_utc(timestr):
    utc_time = parser.parse(timestr)
    local_time = utc_time.replace(tzinfo=datetime.timezone.utc).astimezone(tz=None)
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
    top8_link = get_stage_link(tournament_id, stage_ids[1])
    top8_games = get_stage_games(stage_ids[-1])
    if 'completedAt' not in top8_games[-1]: continue
    match_id = top8_games[-1]['_id']
    finals = json.loads(requests.get(match_info_url % locals()).text)
    finals_name = finals[0]['top']['team']['name']
    winner = finals[0]['top']['team']['name'] if finals[0]['top']['winner'] else finals[0]['bottom']['team']['name']
    print("%s,%s,%s,%s,%s,%s" % (tournament_name.split('-')[-1], date_str, tournament_link_str % locals(), swiss_link, top8_link, winner))
    tmp_final = top8_games[-1]
