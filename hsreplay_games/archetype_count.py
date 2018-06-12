import requests
from datetime import * 
import time
import sys
import MySQLdb
sys.path.append('../')
from config import basedir
sys.path.append(basedir)
sys.path.append(basedir + '/lineupSolver')
from json_cards_to_python import *
from deck_manager import *
from hearthstone import *

url = "https://hsreplay.net/api/v1/live/replay_feed/?format=json&offset=%(offset)s"
game_url = "https://hsreplay.net/api/v1/games/%(game_id)s/?format=json"

connection = MySQLdb.connect(host='localhost', user=db_user, passwd=db_passwd)
cursor = connection.cursor()

sql = """
SELECT archetype1, archetype2
FROM hsreplay.hsreplay
WHERE 
    #(p1_rank like 'L%%' or p2_rank like 'L%%')
    #and 
    (archetype1 like 'Other%%' or archetype2 like 'Other%%')
"""

counts = {}
cursor.execute(sql)
for i, j in cursor.fetchall():
    if 'Other' in i:
        counts[i] = counts.get(i, 0) + 1
    if 'Other' in j:
        counts[j] = counts.get(j, 0) + 1

for i,j in sorted(counts.items(), key = lambda x:x[1]):
    print(i,j)
