#parsing tournament
# 1) Check if tournament is finished (maybe just stage) or loaded
# 2) Parse each stage
# 3) load tournament info into db
# 4) Parse each match
# 5) Check if decks have been loaded
# 6) If they haven't load the lineup for the player and create player_id for tournament
# 7) 

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

cursor.execute("SELECT player_id, tournament_id, archetype_prim, deck1 FROM %(db)s.player_info join %(db)s.tournament using(tournament_id) where time >= 1554861610" % locals())
#cursor.execute("SELECT player_id, tournament_id, archetype_prim, deck1 FROM %(db)s.player_info join %(db)s.tournament using(tournament_id)" % locals())
def update_player(tournament_id, player_id, archetype):
    #player_name = str(player_name.encode('utf-8'))
    db = 'masters_cups'
    archetype = str(archetype).replace("'", '')
    sql = """UPDATE %(db)s.player_info
             SET archetype_prim = "%(archetype)s"
             WHERE player_id = '%(player_id)s' and tournament_id = '%(tournament_id)s'
          """
    #print(len(str(player_name)))
    #print(sql % locals())
    cursor.execute(sql % locals())
    connection.commit()

for p, t, a, d in cursor.fetchall():
    #print(p,t,a,d)
    #update_player(t,p,a)
    archetype = label_archetype(d)
    if a != archetype:
        print(a, archetype)
        #update_player(t,p,archetype)
