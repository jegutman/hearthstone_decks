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
    SELECT p1.player_name as p1, p2.player_name as p2, sum(if(result='W', 1, 0)) as wins, sum(if(result='L', 1, 0)) as losses, sum(1) as games
    FROM %(db)s.games g join %(db)s.tournament t on g.tournament_id = t.tournament_id
        join %(db)s.player_info p1 on t.tournament_id = p1.tournament_id and g.player_id = p1.player_id
        join %(db)s.player_info p2 on t.tournament_id = p2.tournament_id and g.opponent_id = p2.player_id
    #WHERE p1.archetype_prim != p2.archetype_prim
    where p1.player_name < p2.player_name
    GROUP BY p1, p2
    ORDER BY games desc
"""
#print(sql % locals())
cursor.execute(sql % locals())
for a,b,c,d,e in cursor.fetchall()[:50]:
    e = round(float(c) / (float(c) + float(d)) * 100, 1)
    c = str(c)
    d = str(d)
    e = str(e)
    print(",".join([a,b,c,d,e]))
