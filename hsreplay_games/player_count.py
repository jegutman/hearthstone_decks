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

start_date = '2018_05_22'
if len(sys.argv) > 1:
    if len(sys.argv[1]) < 3:
        start_date = (datetime.now() - timedelta(days=int(sys.argv[1]))).strftime("%Y_%m_%d")
    else:
        start_date = sys.argv[1]
print(start_date)

sql = """SELECT %(player)s, result, count(game_id)
         FROM hsreplay.hsreplay
         WHERE (p1_rank like 'L%%' or p2_rank like 'L%%')
            and date >= '%(start_date)s'
         GROUP by %(player)s, result
"""

p_count = {}
p_wins = {}
p_losses = {}
for player in ['p1', 'p2']:
    cursor.execute(sql % locals())
    for p, result, count in cursor.fetchall():
        p = p.strip()
        count = int(count)
        p_count[p] = p_count.get(p, 0) + count
        if player == 'p1':
            if result == 'W':
                p_wins[p] = p_wins.get(p, 0) + count
            else:
                p_losses[p] = p_losses.get(p, 0) + count
        if player == 'p2':
            if result == 'L':
                p_wins[p] = p_wins.get(p, 0) + count
            else:
                p_losses[p] = p_losses.get(p, 0) + count

max_output = 40
for p, count in sorted(p_count.items(), key=lambda x:p_wins.get(x[0], 0), reverse=True)[:200]:
    wr = round(100 * float(p_wins.get(p, 0)) / (p_wins.get(p, 0) + p_losses.get(p, 0)), 1)
    total_games = p_wins.get(p, 0) + p_losses.get(p, 0)
    #if wr > 55 and total_games >= 20:
    if True:
        if max_output > 0:
            print("%-5s %-25s %3s - %3s    %s" % (count, p, p_wins.get(p, 0), p_losses.get(p, 0), wr))
            max_output -= 1
