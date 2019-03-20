import json, requests
from config import API_KEY

summoner_url = 'https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/MegaManMusic?api_key=%(API_KEY)s'
match_history_url = 'https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/%(account_id)s?queue=420&api_key=%(API_KEY)s'
match_info = 'https://na1.api.riotgames.com/lol/match/v4/matches/%(match_id)s?api_key=%(API_KEY)s'

a = json.loads(requests.get(summoner_url % locals()).text)
print(a)

print(a['accountId'])
account_id = a['accountId']

b = json.loads(requests.get(match_history_url % locals()).text)
print(b)

for match in b['matches']:
    match_id = match['gameId']
    c = json.loads(requests.get(match_info % locals()).text)
    break

print('KEYS', c.keys())

for i in c['participantIdentities']:
    print(i)

print(c['participants'][0].keys())
#for i in range(0, 10):
#    print(c['participants'][i]['timeline']['lane'], c['participants'][i]['timeline']['role'], c['participants'][i]['teamId'])
#    #print(c['participants'][i]['timeline'])
#    #'csDiffPerMinDeltas' 'damageTakenPerMinDeltas'
#    print(i, c['participantIdentities'][i]['player']['summonerName'], c['participants'][i]['timeline'].get('csDiffPerMinDeltas', {}).get('0-10', 0), c['participants'][i]['timeline'].get('damageTakenPerMinDeltas', {}).get('0-10', 0))
