import json, requests
from config import API_KEY
import datetime
from champions import *

summoner = 'MegaManMusic'

def get_player_id(match, player):
    try:
        for i in match['participantIdentities']:
            if i['player']['summonerName'] == player:
                return i['participantId'] - 1
    except:
        return 0
    return 0

summoner_url = 'https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/%(summoner)s?api_key=%(API_KEY)s'
match_history_url = 'https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/%(account_id)s?queue=420&api_key=%(API_KEY)s'
match_info = 'https://na1.api.riotgames.com/lol/match/v4/matches/%(match_id)s?api_key=%(API_KEY)s'

a = json.loads(requests.get(summoner_url % locals()).text)

account_id = a['accountId']

b = json.loads(requests.get(match_history_url % locals()).text)

for match in b['matches']:
    champ = champs_by_id.get(match['champion'], "UNKNOWN")
    match_id = match['gameId']
    c = json.loads(requests.get(match_info % locals()).text)
    pid = get_player_id(c, summoner)
    #print('PID', pid, end='\t')
    day = datetime.datetime.fromtimestamp(c['gameCreation'] / 1e3).strftime("%Y-%m-%d %H:%M:%S")
    try:
        print(day, '%-20s' % champ, int(10*c['participants'][pid]['timeline']['creepsPerMinDeltas']['0-10']))
    except:
        continue

