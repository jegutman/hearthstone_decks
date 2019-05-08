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
db = 'masters_cups'
#tournament_number, player = args
bracket = 'swiss'
sql = """
    SELECT p1.archetype_prim as a1, p2.archetype_prim as a2, sum(score1) as wins, sum(score2) as losses, sum(score1 + score2) as games
    FROM %(db)s.games g join %(db)s.tournament t on g.tournament_id = t.tournament_id and g.bracket_id = t.%(bracket)s_bracket
        join %(db)s.player_info p1 on t.tournament_id = p1.tournament_id and g.player_id = p1.player_id
        join %(db)s.player_info p2 on t.tournament_id = p2.tournament_id and g.opponent_id = p2.player_id
    WHERE p1.archetype_prim != p2.archetype_prim
        #and time >= 1554861610
        and time >= 1555736437
    GROUP BY a1, a2
    ORDER BY games desc
"""
#print(sql % locals())
cursor.execute(sql % locals())
for a,b,c,d,e in cursor.fetchall()[:100]:
    if a > b: continue
    e = round(float(c) / (float(c) + float(d)) * 100, 1)
    c = str(c)
    d = str(d)
    e = str(e)
    print(",".join([a,b,c,d,e]))

sql = """
    SELECT p1.archetype_prim as a1, sum(score1) as wins, sum(score2) as losses
    FROM %(db)s.games g join %(db)s.tournament t on g.tournament_id = t.tournament_id and g.bracket_id = t.%(bracket)s_bracket
        join %(db)s.player_info p1 on t.tournament_id = p1.tournament_id and g.player_id = p1.player_id
        join %(db)s.player_info p2 on t.tournament_id = p2.tournament_id and g.opponent_id = p2.player_id
    #WHERE p1.archetype_prim != p2.archetype_prim
    WHERE time >= 1554861610
        and time >= 1555736437
    GROUP BY a1
    ORDER BY wins desc
"""
class_stats = defaultdict(lambda : [0,0])
#print(sql % locals())
cursor.execute(sql % locals())
for a,c,d in cursor.fetchall()[:100]:
    e = round(float(c) / (float(c) + float(d)) * 100, 1)
    c = str(c)
    d = str(d)
    e = str(e)
    deck_class = a.split(' ')[-1]
    class_stats[deck_class][0] += int(c)
    class_stats[deck_class][1] += int(d)
    print(",".join([a,c,d,e]))

for a,j in class_stats.items():
    c, d = j
    e = round(float(c) / (float(c) + float(d)) * 100, 1)
    c = str(c)
    d = str(d)
    e = str(e)
    print(",".join([a,c,d,e]))
#res = [(i,j,k) for (i,j,k) in self.cursor.fetchall()]
#bracket = 'top8'
#print(sql % locals())
#self.cursor.execute(sql % locals())
#res = +[(i,j,k) for (i,j,k) in self.cursor.fetchall()]
##decks = [EasyDeck(i, i) for i in res[0]]
#return res

