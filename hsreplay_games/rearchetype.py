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
                      WHERE archetype1 like '%%%(card_class)s' or archetype2 like '%%%(card_class)s'""" % locals())
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

cursor.execute("SELECT game_id, archetype1, archetype2, p1_deck_code, p2_deck_code, p1_rank, p2_rank FROM hsreplay.hsreplay join hsreplay.hsreplay_decks using(game_id)")
success = 0
total = 0
new = {}
for game_id, archetype1, archetype2, p1_deck_code, p2_deck_code, p1_rank, p2_rank in cursor.fetchall():
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
            reference_class = tmp_deck.get_class().capitalize()
            distances = sorted([(d.get_distance(tmp_deck), d) for d in reference_decks[reference_class]], key=lambda x:x[0])
            if distances[0][0] <= 6:
                success += 1
                #tmp_deck.print_deck()
                #print(side_by_side_diff_lines([tmp_deck, distances[0][1]]))
                #print(distances[0][1].name, distances[0][0])
                #print(archetype1, distances[0][1].name)
            elif distances[0][0] > 10:
                tmp = [d for d in reference_decks[reference_class] if d.name == archetype1]
                #print(len(tmp), [tmp, tmp_deck])
                #if len(tmp) > 0:
                #    print(side_by_side_diff_lines([tmp[0], tmp_deck]))
                #    #tmp_deck.print_deck()
                #else:
                #    tmp_deck.print_deck()
                similar_count = count_similar(tmp_deck)
                if similar_count > 10:
                    print("SIMILAR COUNT:", similar_count, p1_deck_code)
                    print(distances[0][0],' ', p1_deck_code, archetype1)
                    reference_decks[reference_class].append(tmp_deck)
                if len(tmp) > 0:
                    print(side_by_side_diff_lines([tmp[0], tmp_deck]))
            else:
                #print(distances[0][0], p1_deck_code)
                #tmp_deck.print_deck()
                pass
        
print(success, total, total - success)
        
