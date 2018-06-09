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
    start_date = sys.argv[1]

print("Start Date:", start_date)

#cursor.execute("SELECT time, p1, p2, archetype1, archetype2, first, result FROM hsreplay.hsreplay WHERE p1_rank like 'L%' or p2_rank like 'L%' ")
cursor.execute("""SELECT time, p1, p2, archetype1, archetype2, first, result FROM hsreplay.hsreplay 
                  WHERE date >= '%(start_date)s'
                      #and (p1_rank like 'L%%' and p2_rank like 'L%%')
               """ % locals())
#games = []
win_rates = {}
win_rates_first = {'overall' : [0,0]}
win_rates_second = {}
for game_time, p1, p2, archetype1, archetype2, first, result in cursor.fetchall():
    archetype1 = archetype1.strip()
    archetype2 = archetype2.strip()
    #if (game_time, p1, p2) in games or (game_time, p2, p1) in games:
    #    continue
    #games.append((game_time, p1, p2))
    #games.append((game_time, p2, p1))
    pair = (archetype1, archetype2)
    overall = (archetype1, 'overall')
    opp = (archetype2, archetype1)
    opp_overall = (archetype2, 'overall')
    if overall not in win_rates:
        win_rates[overall]        = [0,0]
        win_rates_first[overall]  = [0,0]
        win_rates_second[overall]  = [0,0]
    if opp_overall not in win_rates:
        win_rates[opp_overall]         = [0,0]
        win_rates_first[opp_overall]   = [0,0]
        win_rates_second[opp_overall]   = [0,0]
    if pair not in win_rates:
        win_rates[pair]        = [0,0]
        win_rates[opp]         = [0,0]
        win_rates_first[pair]  = [0,0]
        win_rates_first[opp]   = [0,0]
        win_rates_second[pair] = [0,0]
        win_rates_second[opp]  = [0,0]
    win_rates[pair][1] += 1
    win_rates[overall][1] += 1
    win_rates[opp][1]  += 1
    win_rates[opp_overall][1] += 1
    if result == 'W':
        win_rates[pair][0] += 1
        win_rates[overall][0] += 1
    else:
        win_rates[opp][0] += 1
        win_rates[opp_overall][0] += 1
    if first:
        win_rates_first[pair][1] += 1
        win_rates_first[overall][1] += 1
        win_rates_first['overall'][1] += 1
        win_rates_second[opp][1] += 1
        win_rates_second[opp_overall][1] += 1
        if result == 'W':
            win_rates_first[pair][0] += 1
            win_rates_first[overall][0] += 1
            win_rates_first['overall'][0] += 1
        else:
            win_rates_second[opp][0] += 1
            win_rates_second[opp_overall][0] += 1
    else:
        win_rates_second[pair][1] += 1
        win_rates_second[overall][1] += 1
        win_rates_first[opp][1] += 1
        win_rates_first[opp_overall][1] += 1
        if result == 'W':
            win_rates_second[pair][0] += 1
            win_rates_second[overall][0] += 1
        else:
            win_rates_first[opp][0] += 1
            win_rates_first[opp_overall][0] += 1
            
min_games = 10
for i,j in sorted(win_rates.items(), key=lambda x:x[1][1]):
    wr = round(100 * float(j[0]) / float(j[1]), 1)
    #if wr > 79 or wr < 20:
    a1, a2 = i
    wins, total = j
    if total < min_games:
        continue
    first_win, first_total = win_rates_first.get(i, (0,0))
    wr_first = round(100 * float(first_win) / float(max(first_total, 1)), 1)
    second_win, second_total = win_rates_second.get(i, (0,0))
    wr_second = round(100 * float(second_win) / float(max(second_total, 1)), 1)
    diff = round(wr_first - wr_second, 1)
    if True:
        #a1 = a1.replace(' ', '_')
        #a2 = a2.replace(' ', '_')
        print("%-22s %-22s %5s %5s %5s %5s %5s %5s %5s" % (a1, a2, first_win, first_total, wr_first, second_win, second_total, wr_second, diff))
