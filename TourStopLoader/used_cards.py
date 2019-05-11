import sys
sys.path.append('/home/jgutman/workspace/hearthstone_decks/')
sys.path.append('/home/jgutman/workspace/hearthstone_decks/TourStopLoader')
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
import MySQLdb
import MySQLdb.constants as const
from config import *
connection = MySQLdb.connect(host='localhost', user=db_user, passwd=db_passwd, charset = 'utf8mb4')
#connection = MySQLdb.connect(user = 'guest', db = 'test', charset = 'utf8')
cursor = connection.cursor()
cursor.execute("SET NAMES utf8")
from json_cards_to_python import cards_by_id as cards

sql = "SELECT deck1, deck2, deck3 FROM masters_cups.player_info"
cursor.execute(sql)
card_names = set()
counts = {}
for d1, d2, d3 in cursor.fetchall():
    try:
        for i,j in EasyDeck(d1).deck.cards:
            if cards[i]['set'] not in ['UNGORO', 'ICECROWN', 'LOOTAPALOOZA']:
                name = cards[i]['name']
                card_names.add((name, i))
                counts[name] = counts.get(name, 0) + j
    except:
        pass

for i,j in sorted(counts.items(), key=lambda x:x[1]):
    print(j,i)
