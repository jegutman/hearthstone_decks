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
sql = "SELECT player_name from %(db)s.winners join %(db)s.player_info using(player_id,tournament_id)"
cursor.execute(sql % locals())
winners = [w for (w,) in cursor.fetchall()]
sql = """
    #SELECT p1.player_name, p2.player_name, if(result = 'W', 1, 0)
    SELECT round((pt1.points - pt2.points) / 10, 0) * 10 as diff, sum(if(result = 'W', 1, 0)) as wins, sum(1) as games
    FROM %(db)s.games g
        join %(db)s.player_info p1 on g.tournament_id = p1.tournament_id and g.player_id = p1.player_id
        join %(db)s.player_info p2 on g.tournament_id = p2.tournament_id and g.opponent_id = p2.player_id
        join %(db)s.hct_points pt1 on p1.player_name = pt1.player_name
        join %(db)s.hct_points pt2 on p2.player_name = pt2.player_name
    #WHERE pt2.points > 0 and pt1.points >= 70
    WHERE pt2.points > 20 and pt1.points >= 20
    GROUP BY diff
    HAVING diff > 0
"""
#sql = """
#    SELECT player_name, count(distinct tournament_id), sum(if(result='W', 1, 0)) as wins, sum(if(result='W', 0, 1)) as losses, sum(1) as games
#    FROM %(db)s.games join %(db)s.tournament using (tournament_id) join %(db)s.player_info using(tournament_id, player_id)
#    #WHERE player_name in (SELECT player_name from %(db)s.winners join %(db)s.player_info using(player_id,tournament_id))
#    GROUP BY player_name
#    HAVING games > 60
#    ORDER by games desc
#"""

cursor.execute(sql % locals())
for diff, wins, games in cursor.fetchall():
    print(diff, wins, games)
