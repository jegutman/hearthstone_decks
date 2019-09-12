from summary_urls import *
import datetime
import json, requests

items = json.load(open('/Users/jgutman/workspace/league/item.json'))
tmp = {}
for i,j in items['data'].items():
    #print(i,j)
    tmp[int(i)] = j
    pass
items['data'].update(tmp)
champions = json.load(open('/Users/jgutman/workspace/league/champion.json'))

url_summary = 'https://acs.leagueoflegends.com/v1/stats/game/%(game_key)s'
url_detail  = 'https://acs.leagueoflegends.com/v1/stats/game/%(game_key)s'

summaries = []
timelines = []

def lookup_item(itemId):
    return items['data'][itemId]

def process_event(fn, event, player_map, game_time):
    et = event['type']
    if et == 'BUILDING_KILL':
        #if event['laneType'] == 'MID_LANE' and event['towerType'] == 'OUTER_TURRET':
        if event['towerType'] == 'OUTER_TURRET':
            pass
            #print(event)
            #print(player_map.get(event['teamId']), event['killerId'], player_map.get(event['killerId'] + 5 % 10, 'Unknown').split(' ')[0], player_map.get(event['killerId'], 'Unknown').split(' ')[0], round(event['timestamp'] / 60000, 2))
            # NOTE: teamId is the team whose turret was killed, not team who killed the turret
            #print(game_time, event['laneType'], player_map.get(300 - event['teamId']), player_map.get(event['teamId']), round(event['timestamp'] / 60000, 2))
        return (event['timestamp'], 'TOWER_KILL', player_map.get(300 - event['teamId']), player_map.get(event['teamId']))
    if et == 'CHAMPION_KILL':
        killerId = event['killerId']
        victimId = event['victimId']
        killer = player_map.get(killerId, "Executed")
        victim = player_map[victimId]
        assists = [player_map[i] for i in event['assistingParticipantIds']]
        #print(fn, int(event['timestamp'] / 60000), killer, victim, assists)
        return (event['timestamp'], 'KILL', killer, victim, assists)
    if et == 'ELITE_MONSTER_KILL':
        #print(event)
        killerId = event['killerId']
        killer = player_map.get(killerId, "Executed")
        monster = event.get('monsterSubType', '')
        monster = monster if monster else event['monsterType']
        #print(event['timestamp'], monster, killer)
        return (event['timestamp'], monster, killer)
        pass
    if et == 'ITEM_DESTROYED':
        #return ('ITEM_DESTROYED', event['participantId'], event['itemId'])
        #print(event)
        #item = items['data'][event['itemId']]
        #item_name = item['name']
        #item_cost = item['gold']['total']
        #print(item_cost, item_name)
        pass
    if et == 'ITEM_PURCHASED':
        #return ('ITEM_BOUGHT', event['participantId'], event['itemId'])
        pass
    if et == 'ITEM_SOLD':
        #print(event)
        #return ('ITEM_SOLD', event['participantId'], event['itemId'])
        pass
    if et == 'ITEM_UNDO':
        #print(event)
        pass
    if et == 'SKILL_LEVEL_UP':
        killerId = event['participantId']
        killer = player_map.get(killerId, "Executed")
        if event['levelUpType'] != 'NORMAL':
            #print(event)
            return (event['timestamp'], "SKILL_EVOLVE", killer, event['skillSlot'])
        else:
            return (event['timestamp'], "SKILL_NORMAL", killer, event['skillSlot'])
        pass
    if et == 'WARD_KILL':
        pass
    if et == 'WARD_PLACED':
        pass

def get_game_info(game_key):
    summary_filename = '/Users/jgutman/workspace/hearthstone_decks/lcs/games/summary_' + game_key[14:21] + '_' +  game_key[31:47] + '.json'
    timeline_filename = '/Users/jgutman/workspace/hearthstone_decks/lcs/games/timeline_' + game_key[14:21] + '_' +  game_key[31:47] + '.json'
    try:
        summary = json.load(open(summary_filename))
    except:
        summary = json.loads(requests.get(url_summary % locals()).text)
        json.dump(summary, open(summary_filename, 'w'))
    try:
        timeline = json.load(open(timeline_filename))
    except:
        timeline = json.loads(requests.get((url_detail % locals()).replace('?', '/timeline?')).text)
        json.dump(timeline, open(timeline_filename, 'w'))
    return summary, timeline

def get_team_gold_time(player_status, player_map, times, team):
    total = 0
    opp_total = 0
    for t in times:
        for p in player_status:
            if player_map.get(p, 'zzz zzz').split(' ')[0] == team:
                total += player_status[p][t][0] - player_status[p][max(t-1, 0)][0]
            else:
                opp_total += player_status[p][t][0] - player_status[p][max(t-1, 0)][0]
            #else:
            #    print(player_map.get(p, 'zzz zzz').split(' ')[0], team)
    return total, opp_total
        
def process_timeline(timeline, summary):
    game_time = datetime.datetime.fromtimestamp(summary['gameCreation'] / 1000).strftime("%Y-%m-%dT%H:%M:%S")
    player_map = get_player_map(summary)
    timestamps = []
    player_events = {}
    player_status = {}
    sample_events = []
    # STATUS: GOLD, XP, CS, LVL
    for fn in range(0, len(timeline['frames'])):
        frame  = timeline['frames'][fn]
        timestamps.append(frame['timestamp'])
        for pf in frame['participantFrames'].values():
            pid = pf['participantId']
            pgd = pf['totalGold']
            pxp = pf['xp']
            pcs = pf['minionsKilled']
            plv = pf['level']
            if pid not in player_status:
                player_status[pid] = []
            player_status[pid].append((pgd, pxp, pcs, plv))
        for event in frame['events']:
            pe = process_event(fn, event, player_map, game_time)
            if pid not in player_events:
                player_events[pid] = []
            if pe:
                player_events[pid].append(pe)
            pass
    return player_status, player_events, player_map

def get_player_map(summary):
    team_lookup = {x['participantId'] : x['teamId'] for x in summary['participants']}
    res = {}
    for player_info in summary['participantIdentities']:
        #assert False, player_info['player'].keys()
        res[player_info['participantId']] = player_info['player']['summonerName']
        team = player_info['player']['summonerName'].split(' ')[0]
        res[team_lookup[player_info['participantId']]] = team
    return res

for game_key in summer2019_urls:
    #summary = json.loads(requests.get(url_summary % locals()).text)
    #timeline = json.loads(requests.get((url_detail % locals()).replace('?', '/timeline?')).text)
    summary, timeline = get_game_info(game_key)
    
    summaries.append(summary)
    timelines.append(timeline)
    player_status, player_events, player_map = process_timeline(timeline, summary)

#print(timeline)
