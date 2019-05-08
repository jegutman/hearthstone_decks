import sys
from collections import defaultdict
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
    SELECT p1.archetype_prim as a1, p2.archetype_prim as a2, sum(end_time - start_time) /3600 as match_time, count(start_time) as rounds, sum(score1 + score2) as games
    FROM %(db)s.games g join %(db)s.tournament t on g.tournament_id = t.tournament_id and g.bracket_id = t.%(bracket)s_bracket 
        join %(db)s.times tm on g.tournament_id = tm.tournament_id and g.bracket_id = tm.bracket_id and g.player_id = tm.player_id and g.round_number = tm.round_number
        join %(db)s.player_info p1 on t.tournament_id = p1.tournament_id and g.player_id = p1.player_id
        join %(db)s.player_info p2 on t.tournament_id = p2.tournament_id and g.opponent_id = p2.player_id
    #WHERE p1.archetype_prim != p2.archetype_prim
    #    and time >= 1554861610
    WHERE time >= 1554861610
    GROUP BY a1, a2
    ORDER BY match_time desc
"""
#print(sql % locals())
cursor.execute(sql % locals())
for a,b,c,d,e in cursor.fetchall()[:100]:
    if a > b: continue
    c = float(c)
    d = int(d)
    e = int(e)
    if d < 100: continue
    print("%s,%s,%s,%s,%s" % (a,b,c,d,e))
