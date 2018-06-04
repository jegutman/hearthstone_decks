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

archetypes_url = 'https://hsreplay.net/api/v1/archetypes/?format=json'
archetypes_json = requests.get(archetypes_url).json()

archetype_names = {}
archetype_ids = {}
for archetype in archetypes_json:
    archetype_names[archetype['id']] = archetype['name']
    archetype_ids[archetype['name']] = archetype['id']

def get_archetype(arch_id):
    res = archetype_names.get(int(arch_id))
    return res

games = []
#max_game = 200
offset = 0
game_ids = []
count = 0
game_count = 0
game_infos = {}
while True:
    count += 1
    print("COUNT :", count)
    try:
        tmp_games = requests.get(url % locals()).json()['data']
    except:
        print("Failed to connect")
        time.sleep(120)
        continue
    #mysql> CREATE TABLE hsreplay
    #    -> (
    #    ->     game_id        varchar(22) NOT NULL,
    #    ->     time           int(32) NOT NULL, 
    #    ->     date           varchar(10) NOT NULL,
    #    ->     p1             varchar(32) NOT NULL,
    #    ->     p2             varchar(32) NOT NULL,
    #    ->     archetype1     varchar(32),
    #    ->     archetype2     varchar(32),
    #    ->     p1_rank        varchar(6),
    #    ->     p2_rank        varchar(6),
                # num_turns??
                # ladder_season
                # format
    #    ->     first          boolean NOT NULL,
    #    ->     result         varchar(1) NOT NULL,
    #    ->     PRIMARY KEY(game_id)
    #    -> );
    for game in tmp_games:
        game_id      = game['id']

        if game_id in game_ids: continue
        game_ids.append(game_id)

        p1_rank      = game['player1_rank']
        p2_rank      = game['player2_rank']
        p1_l_rank    = game['player1_legend_rank']
        p2_l_rank    = game['player2_legend_rank']

        
        
        p1_won       = game['player1_won']
        p2_won       = game['player2_won']
        archetype1   = get_archetype(game['player1_archetype'])
        archetype2   = get_archetype(game['player2_archetype'])
        p1_rank = int(p1_rank) if p1_rank != 'None' else 0
        p2_rank = int(p2_rank) if p2_rank != 'None' else 0
        if p1_rank <= 5 or p2_rank <= 5:
            if p1_rank > 0:
                p1_insert_rank = p1_rank
            else:
                p1_insert_rank = 'L' + str(p1_l_rank)
            if p2_rank > 0:
                p2_insert_rank = p2_rank
            else:
                p2_insert_rank = 'L' + str(p2_l_rank)
            try:
                game_count += 1
                game_info = requests.get(game_url % locals()).json()
                time_info = game_info['global_game']['match_start']

                game_time = datetime.strptime(time_info[:19], "%Y-%m-%dT%H:%M:%S").strftime("%s")
                game_date = time_info[:10].replace('-', '_')
                first = 1 if game_info['friendly_player']['is_first'] else 0
                result = 'W' if game_info['won'] else 'L'

                #game_infos[game_id] = game_info
                p1 = game_info['friendly_player']['name']
                p2 = game_info['opposing_player']['name']

                if game_info['friendly_player']['player_id'] != 1:
                    p1, p2 = p2, p1
                    result = 'L' if result == 'W' else 'W'
                    first = 1 - first
                num_turns = game_info['global_game']['num_turns']
                ladder_season = game_info['global_game']['ladder_season']
                game_format = game_info['global_game']['format']
                cursor.execute("""INSERT INTO hsreplay.hsreplay (game_id, time, date, p1, p2, archetype1, archetype2, p1_rank, p2_rank, num_turns, ladder_season, format, first, result)
                                  VALUES ('%(game_id)s', %(game_time)s, '%(game_date)s', '%(p1)s', '%(p2)s', '%(archetype1)s',' %(archetype2)s', '%(p1_insert_rank)s', '%(p2_insert_rank)s', %(num_turns)s, 
                                           %(ladder_season)s, %(game_format)s, %(first)s, '%(result)s')""" % locals())
                connection.commit()
                print("INSERTED: %(p1)-25s %(p2)-25s %(result)s %(archetype1)-25s %(archetype2)-25s" % locals())
                
            except:
                print("SOMETHING FAILED")
                continue
    time.sleep(5)

#counts = {}
#for i,j,k in games:
#    counts[i] = counts.get(i, 0) + 1
#    counts[j] = counts.get(j, 0) + 1
#for i, j in sorted(counts.items(), key=lambda x:x[1], reverse=True):
#    print(j, i)

