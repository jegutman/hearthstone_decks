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
tournaments = { }
official_times = {}
db = 'masters_cups'
cursor.execute("SELECT tournament_id, tournament_name, time from %(db)s.tournament" % locals())
for i,j,k in cursor.fetchall():
    tournaments[i] = j
    official_times[i] = k

file = open('play_time.out')
player_starts = {}
player_ends = {}
game_time = {}
times = []
tournament_starts = {}
tournament_ends = {}
for line in file:
    player, tournament, start_time, end_time = line.strip().split(' ')
    if player not in player_starts:
        player_starts[player] = {}
        player_ends[player] = {}
    if tournament not in player_starts[player]:
        player_starts[player][tournament] = 1e100
        player_ends[player][tournament] = 0
    start_time = int(start_time)
    end_time = int(end_time)
    if end_time - start_time > 10800: end_time = start_time + 10800
    times.append((round((end_time - start_time) / 60, 2), player, tournament))
    game_time[player] = game_time.get(player, 0) + end_time - start_time
    player_starts[player][tournament] = min(player_starts[player][tournament], start_time)
    player_ends[player][tournament] = max(player_ends[player][tournament], end_time)
    tournament_ends[tournament] = max(tournament_ends.get(tournament, 0), end_time)
    tournament_starts[tournament] = min(tournament_starts.get(tournament, 1e99), start_time)

#ttimes = [(round((tournament_ends[i] - tournament_starts[i]) / 3600, 1), tournaments[i]) for i in tournament_ends]
ttimes = [(round((tournament_ends[i] - official_times[i]) / 3600, 1), tournaments[i]) for i in tournament_ends]
print(ttimes)
for i,j in sorted(ttimes, key=lambda x:x[1]):
    print("   %-50s %s" % (j,i))

just_times = [i for i,j in ttimes]
print(round(sum(just_times) / len(just_times), 1))
just_times = [i for i,j in ttimes if int(j.split('-')[-1]) <= 180]
#print(round(sum(just_times) / len(just_times), 1))
just_times = [i for i,j in ttimes if int(j.split('-')[-1]) > 180]
print(round(sum(just_times) / len(just_times), 1))
