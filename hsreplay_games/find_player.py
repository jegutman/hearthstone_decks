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

sql = """SELECT game_id, date, time, p1, p2, p1_rank, p2_rank, archetype1, archetype2, result, p1_deck_code, p2_deck_code
         FROM hsreplay.hsreplay join hsreplay.hsreplay_decks using(game_id)
         WHERE p1 like '%(player_search)s' or p2 like '%(player_search)s'
         ORDER BY time
"""

player_search  = sys.argv[1]
cursor.execute(sql % locals())
total = 0
wins = 0
for game_id, date, time, p1, p2, p1_rank, p2_rank, archetype1, archetype2, result, p1_deck_code, p2_deck_code in cursor.fetchall():
    game_time = datetime.fromtimestamp(time)
    time_string = game_time.strftime("%H:%M:%S")
    game_id = game_id.strip()
    date = date.strip()
    p1 = p1.strip()
    p2 = p2.strip()
    p1_rank = p1_rank.strip()
    p2_rank = p2_rank.strip()
    archetype1 = archetype1.strip()
    archetype2 = archetype2.strip()
    result = result.strip()
    p1_deck_code = p1_deck_code.strip()
    p2_deck_code = p2_deck_code.strip()
    if p2.lower() == player_search.lower():
        p1, p2 = p2, p1
        p1_rank, p2_rank = p2_rank, p1_rank
        archetype1, archetype2 = archetype2, archetype1
        result = 'L' if result == 'W' else 'W'
        p1_deck_code, p2_deck_code = p2_deck_code, p1_deck_code
    if result == 'W':
        wins += 1
    total += 1
    #print("%22s %10s     %-25s %-25s %-25s %-25s %s\n    %-80s\n    %-80s" % (game_id, date, p1, p2, archetype1, archetype2, result, p1_deck_code, p2_deck_code))
    print("%22s %10s %s    %-25s %-25s %-5s %-5s %-25s %-25s %s" % (game_id, date, time_string, p1, p2, p1_rank, p2_rank, archetype1, archetype2, result))
    
if total > 0:
    wr = round(100 * float(wins) / total, 1)
    losses = total - wins
    print("%s - %s     : %s" % (wins, losses, wr))
else:
    print("Did not find games for: %s" % player_search)