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
db = 'masters_cups'
sql = """
    SELECT player_name, time, tournament_name, deck1, deck2, deck3
    FROM %(db)s.player_info join %(db)s.tournament using(tournament_id)
    ORDER BY time
"""
#print(sql % locals())
cursor.execute(sql % locals())

card_name = sys.argv[1]
card_class = sys.argv[2]
print("NAME:",card_name)
first_time = 9 * 10e100
res = []

for name, ttime, tname, d1, d2, d3 in cursor.fetchall():
    if ttime > first_time:
        break
    for tmp_deck in (d1, d2, d3):
        d = EasyDeck(tmp_deck)
        if d.check_card(card_name) and d.get_class().lower() == card_class.lower():
            res.append((name, tname, tmp_deck))
            first_time = ttime

for i in res:
    print(i)
    
