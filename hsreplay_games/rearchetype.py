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

from label_archetype import *

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

reference_decks = {}
cursor.execute("SELECT card_class, archetype, deck_code from hsreplay.reference_archetypes")
for card_class, archetype, deck_code in cursor.fetchall():
    reference_decks[card_class] = reference_decks.get(card_class, []) + [EasyDeck(deck_code, archetype)]

cursor.execute("""SELECT game_id, archetype1, archetype2, p1_deck_code, p2_deck_code, p1_rank, p2_rank FROM hsreplay.hsreplay join hsreplay.hsreplay_decks using(game_id) 
                  #WHERE archetype1 like '%%Priest' or archetype2 like '%%Priest'
                  #WHERE processed = 0
                  #    or (archetype1 like 'Other%%' or archetype2 like 'Other%%')
                  WHERE (archetype1 like '%%Hunter' or archetype2 like '%%Hunter')
                  ORDER BY time""")
#cursor.execute("""SELECT game_id, archetype1, archetype2, p1_deck_code, p2_deck_code, p1_rank, p2_rank FROM hsreplay.hsreplay join hsreplay.hsreplay_decks using(game_id) 
#                  WHERE game_id = 'q9CHmr6s7GywMUWytMVreK'
#                  ORDER BY time""")
success = 0
total = 0
new = {}
updates = {}
count = 0
to_update = cursor.fetchall()
for game_id, archetype1, archetype2, p1_deck_code, p2_deck_code, p1_rank, p2_rank in to_update:
    count += 1
    print(count, '/', len(to_update))
    if p1_deck_code:
        processed = True
        try:
            tmp_deck = EasyDeck(p1_deck_code, game_id + '_p1')
            tmp_deck2 = EasyDeck(p2_deck_code, game_id + '_p1')
            #tmp_deck.print_deck()
            #print(archetype1)
            #if tmp_deck.card_count() < 26:
            #    assert False
            #if tmp_deck2.card_count() < 26:
            #    assert False
        except:
            processed = False
        if processed:
            new_arch1 = label_archetype(tmp_deck, old_archetype=archetype1)
            new_arch2 = label_archetype(tmp_deck2, old_archetype=archetype2)
            if archetype1 != new_arch1:
                #if (archetype1, new_arch1) not in [('Elemental Shaman', 'Shudderwock Shaman'), ('Recruit Hunter', 'Cube Hunter'), ('Shudderwock Shaman', 'Murmuring Shudderwock Shaman'),
                #                                   ('Combo Priest', 'Dragon Combo Priest')]:
                print(game_id, archetype1, new_arch1)
            if archetype2 != new_arch2:
                #if (archetype2, new_arch2) not in [('Elemental Shaman', 'Shudderwock Shaman'), ('Recruit Hunter', 'Cube Hunter'), ('Shudderwock Shaman', 'Murmuring Shudderwock Shaman'),
                #                                   ('Combo Priest', 'Dragon Combo Priest')]:
                print(game_id, archetype2, new_arch2)

            cursor.execute("""UPDATE hsreplay.hsreplay
                              SET archetype1 = '%(new_arch1)s', archetype2 = '%(new_arch2)s', processed = 1
                              WHERE game_id = '%(game_id)s'""" % locals())
            connection.commit()
        
print(success, total, total - success)
        
for i, j in sorted(updates.items(), key=lambda x:x[1]):
    print(j, i)
print(sum(updates.values()))
