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
    SELECT p1.player_name, p2.player_name, if(result = 'W', 1, 0)
    FROM %(db)s.games g
        join %(db)s.player_info p1 on g.tournament_id = p1.tournament_id and g.player_id = p1.player_id
        join %(db)s.player_info p2 on g.tournament_id = p2.tournament_id and g.opponent_id = p2.player_id
"""
#sql = """
#    SELECT player_name, count(distinct tournament_id), sum(if(result='W', 1, 0)) as wins, sum(if(result='W', 0, 1)) as losses, sum(1) as games
#    FROM %(db)s.games join %(db)s.tournament using (tournament_id) join %(db)s.player_info using(tournament_id, player_id)
#    #WHERE player_name in (SELECT player_name from %(db)s.winners join %(db)s.player_info using(player_id,tournament_id))
#    GROUP BY player_name
#    HAVING games > 60
#    ORDER by games desc
#"""

file = open('hct_pts_2018.csv')
points = {}
for line in file:
    tmp = line.strip().split(',')
    points[tmp[0]] = int(tmp[4])

points_vs_none = 0
points_vs_none_games = 0
more_points = 0
more_points_games = 0
more_points_po = 0
more_points_po_games = 0
null = 0
null_games = 0
seventy_plus = 0
seventy_plus_games = 0
seventy_plus_vs_none = 0
seventy_plus_vs_none_games = 0
no_pts = 0
no_pts_games = 0

cursor.execute(sql % locals())
for p1, p2, result in cursor.fetchall():
    pts_p1 = points.get(p1.split('#')[0], 0)
    pts_p2 = points.get(p2.split('#')[0], 0)
    null += result
    null_games += 1
    if pts_p1 > 0 and pts_p2 == 0:
        points_vs_none += result
        points_vs_none_games += 1
    if pts_p1 > pts_p2:
        more_points += result
        more_points_games += 1
    if pts_p1 > pts_p2 > 0:
        more_points_po += result
        more_points_po_games += 1
    if pts_p1 >= 70:
        seventy_plus += result
        seventy_plus_games += 1
    if pts_p1 >= 70 and pts_p2 == 0:
        seventy_plus_vs_none += result
        seventy_plus_vs_none_games += 1
    if pts_p1 == 0:
        no_pts += result
        no_pts_games += 1
    print("%s,%s,%s,%s,%s" % (p1, p2, pts_p1, pts_p2, result))

#pct = points_vs_none / points_vs_none_games
#print("VS_NONE     ", points_vs_none, points_vs_none_games, pct)
#pct = more_points / more_points_games
#print("MORE_PTS    ", more_points, more_points_games, pct)
#pct = more_points_po / more_points_po_games
#print("MORE_PTS_PO ", more_points_po, more_points_po_games, pct)
#pct = seventy_plus / seventy_plus_games
#print("SEVENTY+    ", seventy_plus, seventy_plus_games, pct)
#pct = seventy_plus_vs_none / seventy_plus_vs_none_games
#print("SEVENTY+_V_0", seventy_plus_vs_none, seventy_plus_vs_none_games, pct)
#pct = no_pts / no_pts_games
#print("NO POINTS   ", no_pts, no_pts_games, pct)
#pct = null / null_games
#print("DEFAULT    ", null, null_games, pct)
