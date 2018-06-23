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

def convert(cards):
    res = {}
    for card in cards:
        if card[-2] == 't':
            card = card[:-2]
        if card[-1] == 't':
            card = card[:-1]
        dbfId = card_id_to_dbfId[card]
        res[dbfId] = res.get(dbfId,0) + 1
    cards = [(i,j) for i,j in res.items()]
    return cards

connection = MySQLdb.connect(host='localhost', user=db_user, passwd=db_passwd)
cursor = connection.cursor()

test_deck = sys.argv[1]
reference_deck = EasyDeck(test_deck)
card_class = reference_deck.get_class().capitalize()

cursor.execute("""SELECT game_id, archetype1, archetype2, p1_deck_code, p2_deck_code, p1_rank, p2_rank
                  FROM hsreplay.hsreplay join hsreplay.hsreplay_decks using(game_id) 
                  WHERE archetype1 like '%%%(card_class)s' and (p1_rank like 'L%%' or p2_rank like 'L%%')
              """ % locals())
success = 0
success10 = 0
total = 0
new = {}
close = []
res = cursor.fetchall()
print(len(res))
threshold = 6
for game_id, archetype1, archetype2, p1_deck_code, p2_deck_code, p1_rank, p2_rank in res:
    if p1_deck_code:
        processed = True
        try:
            tmp_deck = EasyDeck(p1_deck_code, game_id + '_p1')
            if tmp_deck.card_count() < 28:
                assert False
        except:
            processed = False
        if processed:
            total += 1
            distance = reference_deck.get_distance(tmp_deck)
            if distance <= threshold:
                success += 1
                print(game_id, p1_rank, p2_rank)
                print(just_diff_lines([reference_deck,tmp_deck]))
                #tmp_deck.print_deck()
                #print(side_by_side_diff_lines([tmp_deck, distances[0][1]]))
                #print(distances[0][1].name, distances[0][0])
                #print(archetype1, distances[0][1].name)
        
print(success, total, total - success)
        
