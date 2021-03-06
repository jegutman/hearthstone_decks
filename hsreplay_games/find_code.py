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
         WHERE (known_p1_deck_code like '%(player_search)s' or known_p2_deck_code like '%(player_search)s' or
                p1_deck_code like '%(player_search)s' or p2_deck_code like '%(player_search)s')
         #    AND (p1_rank like 'L%%' or p2_rank like 'L%%')
         ORDER BY time
"""

player_search  = sys.argv[1]
cursor.execute(sql % locals())
total = 0
wins = 0
total_by_arch = {}
wins_by_arch = {}
game_count = 0
for game_id, date, time, p1, p2, p1_rank, p2_rank, archetype1, archetype2, num_turns, result, p1_deck_code, p2_deck_code in cursor.fetchall():
    game_count += 1
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
    if p2_deck_code.lower() == player_search.lower() or player_search.replace('%', '').lower() in p2.lower():
        p1, p2 = p2, p1
        p1_rank, p2_rank = p2_rank, p1_rank
        archetype1, archetype2 = archetype2, archetype1
        result = 'L' if result == 'W' else 'W'
        p1_deck_code, p2_deck_code = p2_deck_code, p1_deck_code
    if result == 'W':
        wins += 1
        wins_by_arch[archetype1] = wins_by_arch.get(archetype1, 0) + 1
    total += 1
    total_by_arch[archetype1] = total_by_arch.get(archetype1, 0) + 1
    #print("%22s %10s     %-25s %-25s %-25s %-25s %s\n    %-80s\n    %-80s" % (game_id, date, p1, p2, archetype1, archetype2, result, p1_deck_code, p2_deck_code))
    print("%22s %10s %s    %-25s %-25s %-5s %-5s %-25s %-25s %2s %s" % (game_id, date, time_string, p1, p2, p1_rank, p2_rank, archetype1, archetype2, num_turns, result))
    
if total > 0:
    print("\n\n")
    for archetype, a_total in sorted(total_by_arch.items(), key=lambda x:x[1], reverse=True):
        a_wins = wins_by_arch.get(archetype, 0)
        a_losses = a_total - a_wins
        wr = round(100 * float(a_wins) / a_total, 1)
        wl = "%s - %s" % (a_wins, a_losses)
        print("%-25s: %8s : %s" % (archetype, wl, wr))
    wr = round(100 * float(wins) / total, 1)
    losses = total - wins
    wl = "%s - %s" % (wins, losses)
    print("%-25s: %8s : %s" % ('Total', wl, wr))
    #print("%-25s: %s - %s     : %s" % ('Total', wins, losses, wr))
        
else:
    print("Did not find games for: %s" % player_search)
print("Game Count:", game_count)
