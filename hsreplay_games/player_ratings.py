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
from trueskill import *

connection = MySQLdb.connect(host='localhost', user=db_user, passwd=db_passwd)
cursor = connection.cursor()

min_games = 15
start_date = '2018_05_22'
if len(sys.argv) > 1:
    if len(sys.argv[1]) < 3:
        start_date = (datetime.now() - timedelta(days=int(sys.argv[1]))).strftime("%Y_%m_%d")
    else:
        start_date = sys.argv[1]
print('Start Date:', start_date)
if len(sys.argv) > 2:
    min_games = int(sys.argv[2])
print("Min games: %s" % min_games)
region = '%'
if len(sys.argv) > 3:
    region = sys.argv[3]
print('region:', region.replace('%', 'ANY'))

cursor.execute("""SELECT p1, p2, result FROM hsreplay.hsreplay 
                  WHERE date >= '%(start_date)s' 
                     and region like '%(region)s'
                     #and (p1_rank like 'L%%' or p2_rank like 'L%%')
                     #and (p1_rank like 'L%%' or p2_rank like 'L%%' or p1_rank <= 1 or p2_rank <= 1)
                  ORDER BY time
               """ % locals())
rating = {}
games = {}
wins = {}
for p1, p2, result in cursor.fetchall():
    games[p1] = games.get(p1, 0) + 1
    games[p2] = games.get(p2, 0) + 1
    if p1 not in rating:
        if games[p2] >= 5:
            rating[p1] = Rating(mu=rating[p2].mu)
        else:
            rating[p1] = Rating()
    if p2 not in rating:
        if games[p1] >= 5:
            rating[p2] = Rating(mu=rating[p1].mu)
        else:
            rating[p2] = Rating()
    if result == 'W':
        rating[p1], rating[p2] = rate_1vs1(rating[p1], rating[p2])
        wins[p1] = wins.get(p1, 0) + 1
    else:
        rating[p2], rating[p1] = rate_1vs1(rating[p2], rating[p1])
        wins[p2] = wins.get(p2, 0) + 1

top_players = [i for i in sorted(rating.items(), key = lambda x:expose(x[1]), reverse=True) if games[i[0]] >= min_games]
print("   %-15s %-5s %-5s" % ('Player', 'rEst', 'games'))
index = 0
for p, r in top_players[:50]:
    index += 1
    win = wins.get(p, 0)
    losses = games[p] - win
    print("%2s %-15s %-5.2f %4s    %s - %s" % (index, p, expose(r), games[p], win, losses))

#top_players = [i for i in sorted(rating.items(), key = lambda x:expose(x[1]), reverse=True) if games[i[0]] >= 0]
#print("%-15s %-5s %s" % ('Player', 'rEst', 'games'))
#for p, r in top_players[:30]:
#    print("%-15s %-5.2f %s" % (p, expose(r), games[p]))
