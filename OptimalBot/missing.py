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
tournament_number = 43
db = 'masters_cups'
#tournament_number, player = args
tournament_name = "'hearthstone-masters-qualifier-las-vegas-%(tournament_number)s'" % locals()
bracket = 'swiss'
sql = """
    SELECT archetype_prim as a1, deck1, tournament_name
    FROM %(db)s.player_info join %(db)s.tournament using(tournament_id)
    WHERE archetype_prim like 'Other%%'
    ORDER BY time
"""
#print(sql % locals())
cursor.execute(sql % locals())
for a,b,c in cursor.fetchall():
    print(a,b,c)
    EasyDeck(b).print_deck()
#res = [(i,j,k) for (i,j,k) in self.cursor.fetchall()]
#bracket = 'top8'
#print(sql % locals())
#self.cursor.execute(sql % locals())
#res = +[(i,j,k) for (i,j,k) in self.cursor.fetchall()]
##decks = [EasyDeck(i, i) for i in res[0]]
#return res

