import sys
import pycookiecheat
from fake_useragent import UserAgent
sys.path.append('../')
from config import basedir
sys.path.append(basedir)
sys.path.append(basedir + '/lineupSolver')
from shared_utils import *
from json_cards_to_python import *
import itertools
import json
import requests
import datetime

from get_archetypes import *
from hearthstone.deckstrings import Deck
from deck_manager import *

hero_map_inv = {
    7    : 'WARRIOR',
    1066 : 'SHAMAN',
    930  : 'ROGUE',
    671  : 'PALADIN',
    31   : 'HUNTER',
    274  : 'DRUID',
    893  : 'WARLOCK',
    637  : 'MAGE',
    813  : 'PRIEST',
}

hero_ids = {}

for i,j in hero_map_inv.items():
    hero_ids[j] = i


#url_tmp = 'https://hsreplay.net/analytics/query/list_decks_by_opponent_win_rate/?GameType=RANKED_STANDARD&RankRange=LEGEND_THROUGH_FIVE&Region=ALL&TimeRange=CURRENT_EXPANSION'
#url = 'https://hsreplay.net/analytics/query/list_decks_by_opponent_win_rate/?GameType=RANKED_STANDARD&RankRange=LEGEND_THROUGH_FIVE&Region=ALL&TimeRange=CURRENT_EXPANSION'
#url = 'https://hsreplay.net/analytics/query/list_decks_by_opponent_win_rate/?GameType=RANKED_STANDARD&RankRange=LEGEND_ONLY&Region=ALL&TimeRange=LAST_3_DAYS'
#url = 'https://hsreplay.net/analytics/query/list_decks_by_opponent_win_rate/?GameType=RANKED_STANDARD&RankRange=LEGEND_THROUGH_TEN&Region=ALL&TimeRange=LAST_7_DAYS'
#url = 'https://hsreplay.net/analytics/query/list_decks_by_opponent_win_rate/?GameType=RANKED_STANDARD&RankRange=LEGEND_THROUGH_TEN&Region=ALL&TimeRange=CURRENT_EXPANSION'
#url = 'https://hsreplay.net/analytics/query/list_decks_by_opponent_win_rate/?GameType=RANKED_STANDARD&RankRange=LEGEND_ONLY&Region=ALL&TimeRange=CURRENT_PATCH'

#url = 'https://hsreplay.net/analytics/query/list_decks_by_opponent_win_rate/?GameType=RANKED_STANDARD&RankRange=LEGEND_THROUGH_TEN&Region=ALL&TimeRange=CURRENT_EXPANSION'
#url = 'https://hsreplay.net/analytics/query/list_decks_by_opponent_win_rate/?GameType=RANKED_STANDARD&RankRange=ALL&Region=ALL&TimeRange=CURRENT_EXPANSION&PilotExperience=ALL'
url = 'https://hsreplay.net/analytics/query/list_decks_by_win_rate/?GameType=RANKED_STANDARD&RankRange=ALL&Region=ALL&TimeRange=LAST_30_DAYS'
url_base = 'http://hsreplay.net'
#
ua = UserAgent()
#
header = {'User-Agent':str(ua.chrome)}
cookies = pycookiecheat.chrome_cookies(url_base)
#htmlContent = requests.get(url % locals(), cookies = cookies, headers=header)
htmlContent = requests.get(url % locals())
data = json.loads(htmlContent.text)
#data = json.loads(requests.get('https://hsreplay.net/analytics/query/list_decks_by_win_rate/?GameType=RANKED_STANDARD&RankRange=ALL&Region=ALL&TimeRange=LAST_7_DAYS').text)
#data = json.loads(requests.get('https://hsreplay.net/analytics/query/list_decks_by_opponent_win_rate/?GameType=RANKED_STANDARD&RankRange=ALL&Region=ALL&TimeRange=CURRENT_PATCH&PilotExperience=ALL').text)
#data = json.loads('decks.json')

#data['series']['data']['WARLOCK'][0]['deck_list']
class_data = {}
archetypes = {}
all_decks = []
deck_data = {}
for deck_class in data['series']['data']:
    class_data[deck_class] = data['series']['data'][deck_class]
    for hs_deck in data['series']['data'][deck_class]:
        dd = [hs_deck['win_rate'], hs_deck['total_games']]
        d = Deck()
        cards = eval(hs_deck['deck_list'])
        d.cards = cards
        d.heroes = [hero_ids[deck_class]]
        archetype_id = hs_deck['archetype_id']
        all_decks.append((d, get_archetype(archetype_id, 'None')))
        deck_data[d.as_deckstring] = dd
        archetypes[get_archetype(archetype_id)] = archetypes.get(get_archetype(archetype_id), []) + [d.as_deckstring]
        #print(d.as_deckstring)
#print(archetypes)
    #EasyDeck(ds).print_deck()

all_decks = [EasyDeck(i.as_deckstring, j) for i,j in all_decks]
    
#url = 'https://hsreplay.net/analytics/query/single_deck_mulligan_guide/?GameType=RANKED_STANDARD&RankRange=LEGEND_ONLY&Region=ALL&deck_id=KAiGarK6LTQMXNTKENBpIg'
#url = 'https://hsreplay.net/analytics/query/single_deck_mulligan_guide/?GameType=RANKED_STANDARD&RankRange=LEGEND_ONLY&Region=ALL&deck_id=I5UH3cUUGnGxgU7SDqc9Sh'
#url = 'https://hsreplay.net/analytics/query/single_deck_mulligan_guide/?GameType=RANKED_STANDARD&RankRange=LEGEND_ONLY&Region=ALL&deck_id=DVQIo0iEDTUhMVYdlWAOMc'

#htmlContent = requests.get(url, cookies = cookies, headers=header)
#a = json.loads(htmlContent.text)
#for i in sorted(a['series']['data']['ALL'], key=lambda x:x['times_in_opening_hand'], reverse=True):
#    print("%5s %5s %5s %s" % (i['times_kept'], i['times_in_opening_hand'], i['times_presented_in_initial_cards'], cards_by_id[i['dbf_id']].get('name')))

for deck_archetype in archetypes:
    if deck_archetype is None: continue
    deck_class = deck_archetype.split(' ')[-1]
    for code in archetypes[deck_archetype]:
        print(",".join([str(i) for i in [deck_class, deck_archetype, code]]))
