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

topX = 10
if len(sys.argv) > 1:
    topX = int(sys.argv[1])
start_date = '2018_05_22'
if len(sys.argv) > 2:
    if len(sys.argv[2]) < 3:
        start_date = (datetime.now() - timedelta(days=int(sys.argv[2]))).strftime("%Y_%m_%d")
    else:
        start_date = sys.argv[2]
print(start_date)


sql = """SELECT game_id, date, time, p1, p2, p1_rank, p2_rank, archetype1, archetype2, num_turns, result, p1_deck_code, p2_deck_code, first
         FROM hsreplay.hsreplay join hsreplay.hsreplay_decks using(game_id)
         WHERE (p1_rank rlike '^L[0-9]?[0-9]$' or p2_rank rlike '^L[0-9]?[0-9]$')
             AND date >= '%(start_date)s'
         ORDER BY time
"""

player_search  = ''
cursor.execute(sql % locals())
total = 0
wins = 0
total_by_arch = {}
wins_by_arch = {}
total_by_player = {}
wins_by_player = {}
games = []
for game_id, date, time, p1, p2, p1_rank, p2_rank, archetype1, archetype2, num_turns, result, p1_deck_code, p2_deck_code, first in cursor.fetchall():
    if (p1, p2, time) in games or (p2, p1, time) in games:
        continue
    games.append((p1, p2, time))
    game_id = game_id.strip()
    game_time = datetime.fromtimestamp(time - 3600 * 5)
    time_string = game_time.strftime("%Y_%m_%d %H:%M:%S")
    date, time_string = time_string.split(' ')
    p1 = p1.strip()
    p2 = p2.strip()
    p1_rank = p1_rank.strip()
    p2_rank = p2_rank.strip()
    #if int(p1_rank.replace('L', '')) > topX and int(p2_rank.replace('L', '')) > topX: continue
    if int(p1_rank.replace('L', '')) <= topX and p1_rank[0] == 'L':
        pass
    elif int(p2_rank.replace('L', '')) <= topX and p2_rank[0] == 'L':
        pass
    else:
        continue
    
    if p1_rank[0] == 'L':
        p1_rank_compare = -100000 + int(p1_rank[1:])
    else:
        p1_rank_compare = int(p1_rank)
    if p2_rank[0] == 'L':
        p2_rank_compare = -100000 + int(p2_rank[1:])
    else:
        p2_rank_compare = int(p2_rank)
    archetype1 = archetype1.strip()
    archetype2 = archetype2.strip()
    result = result.strip()
    num_turns = int(num_turns)
    p1_deck_code = p1_deck_code.strip()
    p2_deck_code = p2_deck_code.strip()
    if p2_rank_compare < p1_rank_compare:
        p1, p2 = p2, p1
        p1_rank, p2_rank = p2_rank, p1_rank
        archetype1, archetype2 = archetype2, archetype1
        result = 'L' if result == 'W' else 'W'
        p1_deck_code, p2_deck_code = p2_deck_code, p1_deck_code
        first = 1 - first
    if result == 'W':
        wins_by_arch[archetype1] = wins_by_arch.get(archetype1, 0) + 1
        wins_by_player[p1] = wins_by_player.get(p1, 0) + 1
    else:
        if 'L' in p2_rank and int(p2_rank.replace('L', '')) <= topX:
            wins_by_arch[archetype2] = wins_by_arch.get(archetype2, 0) + 1
            wins_by_player[p2] = wins_by_player.get(p2, 0) + 1
        pass
    total +=1
    total_by_arch[archetype1] = total_by_arch.get(archetype1, 0) + 1
    total_by_player[p1] = total_by_player.get(p1, 0) + 1
    if 'L' in p2_rank and int(p2_rank.replace('L', '')) <= topX:
        total_by_arch[archetype2] = total_by_arch.get(archetype2, 0) + 1
        total_by_player[p2] = total_by_player.get(p2, 0) + 1
    #print("%22s %10s     %-25s %-25s %-25s %-25s %s\n    %-80s\n    %-80s" % (game_id, date, p1, p2, archetype1, archetype2, result, p1_deck_code, p2_deck_code))
    print("%22s %10s %s    %-25s %-5s %-25s %-5s %-5s %-25s %-25s %2s %s" % (game_id, date, time_string, p1, result, p2, p1_rank, p2_rank, archetype1, archetype2, num_turns, first))
    
print("\n\n")
for player, a_total in sorted(total_by_player.items(), key=lambda x:wins_by_player.get(x[0], 0), reverse=True)[:15]:
    a_wins = wins_by_player.get(player, 0)
    a_losses = a_total - a_wins
    wr = round(100 * float(a_wins) / a_total, 1)
    wl = "%s - %s" % (a_wins, a_losses)
    print("%-25s: %8s : %s" % (player, wl, wr))
print("TOTAL:", total)

print("\n\n")
for archetype, a_total in sorted(total_by_arch.items(), key=lambda x:wins_by_arch.get(x[0], 0), reverse=True)[:20]:
    a_wins = wins_by_arch.get(archetype, 0)
    a_losses = a_total - a_wins
    wr = round(100 * float(a_wins) / a_total, 1)
    wl = "%s - %s" % (a_wins, a_losses)
    print("%-25s: %8s : %s" % (archetype, wl, wr))
print("TOTAL:", total)
