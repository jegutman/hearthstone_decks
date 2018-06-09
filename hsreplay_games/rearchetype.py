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

times_run = 0
def count_similar(reference_deck):
    global times_run, total
    times_run += 1
    print("Times Run:", times_run, total)
    card_class = reference_deck.get_class().capitalize()

    cursor.execute("""SELECT game_id, archetype1, archetype2, p1_deck_code, p2_deck_code 
                      FROM hsreplay.hsreplay join hsreplay.hsreplay_decks using(game_id) 
                      WHERE archetype1 like '%%%(card_class)s' or archetype2 like '%%%(card_class)s'
                      #    AND p1_rank like 'L%%' or p2_rank like 'L%%'
        """ % locals())
    res = cursor.fetchall()
    success = 0
    threshold = 6
    for game_id, archetype1, archetype2, p1_deck_code, p2_deck_code in res:
        if archetype2.split(' ')[-1] == card_class and archetype1.split(' ')[-1] != card_class:
            archetype1, archetype2 = archetype2, archetype1
            p1_deck_code, p2_deck_code = p2_deck_code, p1_deck_code
        if p1_deck_code:
            processed = True
            try:
                tmp_deck = EasyDeck(p1_deck_code, game_id + '_p1')
                if tmp_deck.card_count() < 28:
                    assert False
            except:
                processed = False
            if processed:
                distance = reference_deck.get_distance(tmp_deck)
                if distance <= threshold:
                    success += 1
    return success

cursor.execute("""SELECT game_id, archetype1, archetype2, p1_deck_code, p2_deck_code, p1_rank, p2_rank FROM hsreplay.hsreplay join hsreplay.hsreplay_decks using(game_id) 
                  WHERE processed = 0 
                  ORDER BY time""")
test_id = 'q9CHmr6s7GywMUWytMVreK'
#cursor.execute("""SELECT game_id, archetype1, archetype2, p1_deck_code, p2_deck_code, p1_rank, p2_rank FROM hsreplay.hsreplay join hsreplay.hsreplay_decks using(game_id) 
#                  WHERE game_id = 'q9CHmr6s7GywMUWytMVreK'
#                  ORDER BY time""")
success = 0
total = 0
new = {}
updates = {}
for game_id, archetype1, archetype2, p1_deck_code, p2_deck_code, p1_rank, p2_rank in cursor.fetchall()[-2000:]:
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
            total += 1
            reference_class = tmp_deck.get_class().capitalize()
            #print(reference_class)
            distances = sorted([(d.get_distance(tmp_deck), d) for d in reference_decks[reference_class]], key=lambda x:x[0])
            #print(distances)
            new_arch1 = archetype1
            new_arch2 = archetype2
            if distances[0][0] <= 6:
                success += 1
                #tmp_deck.print_deck()
                #print(side_by_side_diff_lines([tmp_deck, distances[0][1]]))
                #print(distances[0][1].name, distances[0][0])
                new_arch1 = distances[0][1].name
                #print('test', new_arch1)
                if archetype1 != new_arch1:
                    if (archetype1, new_arch1) not in [('Elemental Shaman', 'Shudderwock Shaman'), ('Recruit Hunter', 'Cube Hunter'), ('Shudderwock Shaman', 'Murmuring Shudderwock Shaman'),
                                                      ('Combo Priest', 'Dragon Combo Priest')]:
                        print(game_id, archetype1, new_arch1)
                    updates[(archetype1, new_arch1)] = updates.get((archetype1, new_arch1), 0) + 1
            elif distances[0][0] > 10:
                pass
                #tmp = [d for d in reference_decks[reference_class] if d.name == archetype1]
                #similar_count = count_similar(tmp_deck)
                #if similar_count > 10:
                #    print("SIMILAR COUNT:", similar_count, p1_deck_code)
                #    print(distances[0][0],' ', p1_deck_code, archetype1)
                #    reference_decks[reference_class].append(tmp_deck)
                #if len(tmp) > 0:
                #    print(side_by_side_diff_lines([tmp[0], tmp_deck]))
            else:
                #print(distances[0][0], p1_deck_code)
                #tmp_deck.print_deck()
                pass

            #2nd deck
            total += 1
            reference_class = tmp_deck2.get_class().capitalize()
            distances = sorted([(d.get_distance(tmp_deck2), d) for d in reference_decks[reference_class]], key=lambda x:x[0])
            if distances[0][0] <= 6:
                success += 1
                #tmp_deck2.print_deck()
                #print(side_by_side_diff_lines([tmp_deck2, distances[0][1]]))
                #print(distances[0][1].name, distances[0][0])
                new_arch2 = distances[0][1].name
                if archetype2 != new_arch2:
                    if (archetype2, new_arch2) not in [('Elemental Shaman', 'Shudderwock Shaman'), ('Recruit Hunter', 'Cube Hunter'), ('Shudderwock Shaman', 'Murmuring Shudderwock Shaman'),
                                                      ('Combo Priest', 'Dragon Combo Priest')]:
                        print(game_id, archetype2, new_arch2)
                    updates[(archetype2, new_arch2)] = updates.get((archetype2, new_arch2), 0) + 1
            cursor.execute("""UPDATE hsreplay.hsreplay
                              SET archetype1 = '%(new_arch1)s', archetype2 = '%(new_arch2)s', processed = 1
                              WHERE game_id = '%(game_id)s'""" % locals())
            connection.commit()
        
print(success, total, total - success)
        
for i, j in sorted(updates.items(), key=lambda x:x[1]):
    print(j, i)
print(sum(updates.values()))
