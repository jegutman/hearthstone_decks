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

cursor.execute("SELECT time, p1, p2, archetype1, archetype2, first, result FROM hsreplay.hsreplay")
games = []
win_rates = {}
win_rates_first = {}
win_rates_second = {}
for game_time, p1, p2, archetype1, archetype2, first, result in cursor.fetchall():
    archetype1 = archetype1.strip()
    archetype2 = archetype2.strip()
    if (game_time, p1, p2) in games or (game_time, p2, p1) in games:
        continue
    games.append((game_time, p1, p2))
    games.append((game_time, p2, p1))
    pair = (archetype1, archetype2)
    opp = (archetype2, archetype1)
    if pair not in win_rates:
        win_rates[pair]        = [0,0]
        win_rates[opp]         = [0,0]
        win_rates_first[pair]  = [0,0]
        win_rates_first[opp]   = [0,0]
        win_rates_second[pair] = [0,0]
        win_rates_second[opp]  = [0,0]
    win_rates[pair][1] += 1
    win_rates[opp][1]  += 1
    if result == 'W':
        win_rates[pair][0] += 1
    else:
        win_rates[opp][0] += 1
    if first:
        win_rates_first[pair][1] += 1
        win_rates_second[opp][1] += 1
        if result == 'W':
            win_rates_first[pair][0] += 1
        else:
            win_rates_second[opp][0] += 1
    else:
        win_rates_second[pair][1] += 1
        win_rates_first[opp][1] += 1
        if result == 'W':
            win_rates_second[pair][0] += 1
        else:
            win_rates_first[opp][0] += 1
            
for i,j in sorted(win_rates.items(), key=lambda x:x[1][1]):
    wr = round(100 * float(j[0]) / float(j[1]), 1)
    if wr > 79 or wr < 20:
        print(i,j, wr)
