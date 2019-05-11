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
    SELECT player_name, count(distinct tournament_id) as cups, sum(if(result='W', 1, 0)) as wins, sum(if(result in ('W', 'L'), 1, 0)) as games, sum(if(result='W', 1, 0)) /sum(if(result in ('W', 'L'), 1, 0)) as pct
    FROM masters_cups.games join masters_cups.player_info using(tournament_id, player_id)
    WHERE player_name like '%%'
        and player_name in (SELECT player_name from %(db)s.winners join %(db)s.player_info using(tournament_id, player_id))
    GROUP BY player_name
    HAVING games > 80
    ORDER BY wins desc, cups desc
"""
#print(sql % locals())
cursor.execute(sql % locals())
for a,b,c,d,e in cursor.fetchall():
    b = str(b)
    c = str(c)
    d = str(d)
    e = str(e)
    print(",".join([a,b,c,d,e]))
#res = [(i,j,k) for (i,j,k) in self.cursor.fetchall()]
#bracket = 'top8'
#print(sql % locals())
#self.cursor.execute(sql % locals())
#res = +[(i,j,k) for (i,j,k) in self.cursor.fetchall()]
##decks = [EasyDeck(i, i) for i in res[0]]
#return res

