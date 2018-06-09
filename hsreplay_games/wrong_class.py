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

from get_archetype import *

url = "https://hsreplay.net/api/v1/live/replay_feed/?format=json&offset=%(offset)s"
game_url = "https://hsreplay.net/api/v1/games/%(game_id)s/?format=json"

connection = MySQLdb.connect(host='localhost', user=db_user, passwd=db_passwd)
cursor = connection.cursor()

sql = """
SELECT game_id, archetype1, archetype2, p1_deck_code, p2_deck_code
FROM hsreplay.hsreplay join hsreplay.hsreplay_decks using(game_id)
#WHERE p1_rank like 'L%%' or p2_rank like 'L%%'
"""
cursor.execute(sql % locals())
count = 0
total = 0
for game_id, archetype1, archetype2, p1_deck_code, p2_deck_code in cursor.fetchall():
    total += 2
    try:
        deck1 = EasyDeck(p1_deck_code)
        if archetype1.split(' ')[-1] != deck1.get_class():
            new_arch  = get_archetype(deck1, old_archetype = 'Other ' + deck1.get_class(), threshold=10)
            print("%s %s %-10s %-25s %-25s" % (game_id, 1, deck1.get_class(), archetype1, new_arch))
            count += 1
            cursor.execute("""UPDATE hsreplay.hsreplay
                              SET archetype1 = '%(new_arch)s'
                              WHERE game_id = '%(game_id)s'""" % locals())
            connection.commit()
    except:
        print(p1_deck_code)
    try:
        deck2 = EasyDeck(p2_deck_code)
        if archetype2.split(' ')[-1] != deck2.get_class():
            new_arch  = get_archetype(deck2, old_archetype = 'Other ' + deck2.get_class(), threshold=10)
            print("%s %s %-10s %-25s %-25s" % (game_id, 2, deck2.get_class(), archetype2, get_archetype(deck2, old_archetype = 'Other ' + deck2.get_class(), threshold=10)))
            count += 1
            cursor.execute("""UPDATE hsreplay.hsreplay
                              SET archetype2 = '%(new_arch)s'
                              WHERE game_id = '%(game_id)s'""" % locals())
            connection.commit()
    except:
        print(p2_deck_code)

print(count, total)
