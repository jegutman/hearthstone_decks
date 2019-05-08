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
#tournament_number, player = args
#tournament_name = "'hearthstone-masters-qualifier-las-vegas-%(tournament_number)s'" % locals()
bracket = 'swiss'
sql = """
    SELECT t.tournament_name as tn, p1.player_name as p1_name, sum(if(result='W', 1, 0)) as wins, sum(if(result='W', 0, 1)) as losses, sum(score1 + score2) as games
    FROM %(db)s.games g join %(db)s.tournament t on g.tournament_id = t.tournament_id and g.bracket_id = t.swiss_bracket
        join %(db)s.player_info p1 on t.tournament_id = p1.tournament_id and g.player_id = p1.player_id
    #WHERE p1.archetype_prim != p2.archetype_prim
    GROUP BY tn, p1_name
    #HAVING wins >= 5
    ORDER BY tn, p1_name
"""
#print(sql % locals())
from collections import defaultdict
count = defaultdict(lambda : 0)
cursor.execute(sql % locals())
for a,b,c,d,e in cursor.fetchall():
    if int(d) == 0:
        count[a] += 1
    count[a] += 0
    c = str(c)
    d = str(d)
    e = str(e)
    print(",".join([a,b,c,d,e]))

for i,j in count.items():
    if j == 0:
        print(i)
#res = [(i,j,k) for (i,j,k) in self.cursor.fetchall()]
#bracket = 'top8'
#print(sql % locals())
#self.cursor.execute(sql % locals())
#res = +[(i,j,k) for (i,j,k) in self.cursor.fetchall()]
##decks = [EasyDeck(i, i) for i in res[0]]
#return res

