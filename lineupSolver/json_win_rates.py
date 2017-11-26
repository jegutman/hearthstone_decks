import json
import requests
filename = 'hsreplay1126.json'
print "using:", filename
wr_file = open(filename)

from get_archetypes import *

#r = requests.get('https://hsreplay.net/analytics/query/head_to_head_archetype_matchups/?GameType=RANKED_STANDARD&RankRange=LEGEND_THROUGH_FIVE&Region=ALL&TimeRange=LAST_7_DAYS')
#wr_json = json.loads(r.content)

win_pcts = {}
num_games = {}
hsreplay_archetypes = []
#min_game_threshold = 200
min_game_threshold = 0
wr_json = json.load(wr_file)
game_count = {}
for a1 in wr_json['series']['data'].keys():
    arch1 = get_archetype(a1.strip())
    if arch1 not in hsreplay_archetypes:
        hsreplay_archetypes.append(arch1)
        game_count[arch1] = 0
    for a2 in wr_json['series']['data'][a1].keys():
        arch2 = get_archetype(a2)
        wr, total_games = wr_json['series']['data'][a1][a2]['win_rate'], wr_json['series']['data'][a1][a2]['total_games']
        if total_games >= min_game_threshold:
            win_pcts[(arch1, arch2)] = wr
        num_games[(arch1, arch2)] = total_games
        game_count[arch1] += total_games

#archetype_names = {}
#for archetype in archetypes_json:
#    archetype_names[archetype['id']] = archetype['name']

##cards_by_raw_id = {}
#for card in cards_json:
#    #if 'id' in card and 'set' in card and card.get('collectible', False):
#    cards_by_raw_id[card['id']] = card
#
#card_name_to_id = {}
#for card in cards_json:
#    if 'dbfId' in card and 'set' in card and card.get('collectible', False):
#        card_name_to_id[card['name']] = card['dbfId']
#
#names = {}
#for card in cards_json:
#    if 'dbfId' in card and 'name' in card and 'set' in card and card.get('collectible', False) == True:
#        name = card['name']
#        if name not in names:
#            names[name] = []
#        names[name].append(card['dbfId'])
#
#hero_powers = {}
#for card in cards_json:
#    if 'type' in card:
#        if card['type'] == 'HERO_POWER':
#            hero_powers[card['id']] = card
#
#def lookup_card_name(card):
#    if 'card_id' not in dir(card): return "Not Card"
#    if card.card_id is None: return "Unknown Card"
#    return cards_by_raw_id[card.card_id]['name']
