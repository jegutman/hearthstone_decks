import sys
sys.path.append('../')
from config import basedir
sys.path.append(basedir)
sys.path.append(basedir + '/lineupSolver')
#from backports import csv
from datetime import datetime
from hearthstone.deckstrings import Deck
from hearthstone.deckstrings import FormatType
import json
import os
import re
import requests
from deck_manager import *
#from conquest_utils import *

players_url = 'https://webapi.worldgaming.com/api/k28aw4xmV3IZ294/cpu/tournaments/1745/users?order_by=name&page=1&page_size=400'

players_data = json.loads(requests.get(players_url).text)

entries = players_data['page']['entries']
players = []
plookup = {}
for entry in entries:
    user_id = entry['user_id']
    player = entry['metadata']['gamertag']
    player = player.split('#')[0].strip()
    plookup[user_id] = player
    players.append((user_id, player))

decks_url = 'https://webapi.worldgaming.com/api/k28aw4xmV3IZ294/cpu/tournaments/1745/user/%(user_id)s/decks'
player_decks = {}
for user_id, player in players:
    player_decks[player] = []
    deck_data = json.loads(requests.get(decks_url % locals()).text)
    for deck in deck_data['data']:
        d = Deck()
        for i in deck['cards']:
            d.format = FormatType.FT_STANDARD
            card_id = i['dbfId']
            copies = i['copies']
            if copies == 0:
                d.heroes = [card_id]
            else:
                d.cards.append((card_id, copies))
        player_decks[player].append(d.as_deckstring)

def print_player(player):
    global player_decks
    for i in print_side_by_side([EasyDeck(j) for j in player_decks[player]]):
        print(i)

