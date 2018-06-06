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

sql = """SELECT game_id, date, time, p1, p2, p1_rank, p2_rank, archetype1, archetype2, num_turns, result, p1_deck_code, p2_deck_code
         FROM hsreplay.hsreplay join hsreplay.hsreplay_decks using(game_id)
         WHERE ((archetype1 like '%(qry_archetype1)s' AND archetype2 like '%(qry_archetype2)s') OR (archetype1 like '%(qry_archetype2)s' AND archetype2 like '%(qry_archetype1)s'))
             #AND (p1_rank rlike '^L[0-9]?[0-9]$' or p2_rank rlike '^L[0-9]?[0-9]$')
         ORDER BY time
"""

qry_archetype1  = sys.argv[1]
qry_archetype2  = sys.argv[2]
cursor.execute(sql % locals())
total = 0
wins = 0
total_by_player = {}
wins_by_player = {}
for game_id, date, time, p1, p2, p1_rank, p2_rank, archetype1, archetype2, num_turns, result, p1_deck_code, p2_deck_code in cursor.fetchall():
    game_id = game_id.strip()
    game_time = datetime.fromtimestamp(time - 3600 * 5)
    time_string = game_time.strftime("%Y_%m_%d %H:%M:%S")
    date, time_string = time_string.split(' ')
    p1 = p1.strip()
    p2 = p2.strip()
    p1_rank = p1_rank.strip()
    p2_rank = p2_rank.strip()
    archetype1 = archetype1.strip()
    archetype2 = archetype2.strip()
    result = result.strip()
    num_turns = int(num_turns)
    p1_deck_code = p1_deck_code.strip()
    p2_deck_code = p2_deck_code.strip()
    if archetype2.lower() == qry_archetype1.lower() or qry_archetype1.replace('%', '').lower() in archetype2.lower():
        p1, p2 = p2, p1
        p1_rank, p2_rank = p2_rank, p1_rank
        archetype1, archetype2 = archetype2, archetype1
        result = 'L' if result == 'W' else 'W'
        p1_deck_code, p2_deck_code = p2_deck_code, p1_deck_code
    if result == 'W':
        wins += 1
        wins_by_player[p1] = wins_by_player.get(p1, 0) + 1
    total += 1
    total_by_player[p1] = total_by_player.get(p1, 0) + 1
    #print("%22s %10s     %-25s %-25s %-25s %-25s %s\n    %-80s\n    %-80s" % (game_id, date, p1, p2, archetype1, archetype2, result, p1_deck_code, p2_deck_code))
    print("%22s %10s %s    %-25s %-25s %-5s %-5s %-25s %-25s %2s %s" % (game_id, date, time_string, p1, p2, p1_rank, p2_rank, archetype1, archetype2, num_turns, result))
    
if total > 0:
#    print("\n\n")
#    for p, a_total in sorted(total_by_player.items(), key=lambda x:x[1], reverse=True):
#        a_wins = wins_by_player.get(p, 0)
#        a_losses = a_total - a_wins
#        wr = round(100 * float(a_wins) / a_total, 1)
#        wl = "%s - %s" % (a_wins, a_losses)
#        print("%-25s: %8s : %s" % (p, wl, wr))
    wr = round(100 * float(wins) / total, 1)
    losses = total - wins
    wl = "%s - %s" % (wins, losses)
    print("%-25s: %8s : %s" % ('Total', wl, wr))
#    #print("%-25s: %s - %s     : %s" % ('Total', wins, losses, wr))
        
