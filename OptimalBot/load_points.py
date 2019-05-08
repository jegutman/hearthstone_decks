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
    SELECT distinct player_name
    FROM %(db)s.player_info
"""
file = open('hct_pts_2018.csv')
points = {}
for line in file:
    tmp = line.strip().split(',')
    points[tmp[0]] = int(tmp[4])

def load_points(player_name, points):
    #player_name = str(player_name.encode('utf-8'))
    db = 'masters_cups'
    sql = """INSERT INTO %(db)s.hct_points (player_name, points)
             VALUES ('%(player_name)s', %(points)s)
             ON DUPLICATE KEY UPDATE
             points = %(points)s;
          """
    cursor.execute(sql % locals())
    connection.commit()

cursor.execute(sql % locals())
for (p,) in cursor.fetchall():
    load_points(p, points.get(p.split('#')[0], 0))
    #print(p)

