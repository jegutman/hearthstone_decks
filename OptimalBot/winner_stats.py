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
sql = """SELECT player_id, player_name from %(db)s.winners join %(db)s.player_info using(tournament_id, player_id) join %(db)s.tournament using(tournament_id) order by time"""
cursor.execute(sql % locals())
stat_sql = """
    SELECT player_name, sum(if(result='W', 1, 0)) as wins, sum(if(result in ('W', 'L'), 1, 0)) as games
    FROM %(db)s.games join %(db)s.player_info using(tournament_id, player_id)
    WHERE player_name = '%(name)s'
    GROUP BY player_name
    ORDER BY wins desc
"""

for (pid, name) in cursor.fetchall():
    cursor.execute(stat_sql % locals())
    for (name, wins, games) in cursor.fetchall():
        pct = round( 100 * float(wins)/ float(games), 1)
        losses = games - wins
        print("%-20s %3s %3s %s" % (name, wins, losses, pct))
