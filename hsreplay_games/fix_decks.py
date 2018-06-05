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
        if card == 'GAME_005':
            continue
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
count = 0

def check_update(game_id, total):
    global count
    count +=1
    print(count, '/', total, game_id)
    game_url = 'https://hsreplay.net/api/v1/games/%(game_id)s/?format=json'
    game_info = requests.get(game_url % locals()).json()

    try:
        first = 1 if game_info['friendly_player']['is_first'] else 0
    except:
        return

    #game_infos[game_id] = game_info
    p1 = game_info['friendly_player']['name']
    p2 = game_info['opposing_player']['name']

    #try:
    if True:
        friendly_cards = []
        known_friendly_cards = []
        if game_info['friendly_deck']['cards']: friendly_cards += game_info['friendly_deck']['cards']
        if game_info['friendly_deck']['cards']: known_friendly_cards += game_info['friendly_deck']['cards']
        if game_info['friendly_deck']['predicted_cards']: friendly_cards = game_info['friendly_deck']['predicted_cards']
        friendly_heroes = [card_id_to_dbfId[game_info['friendly_player']['hero_id']]]
        
        friendly_deck = deckstrings.Deck()
        friendly_deck.cards = convert(friendly_cards)
        friendly_deck.heroes = friendly_heroes
        friendly_deck.format = 2
        friendly_deckstring = friendly_deck.as_deckstring
        p1_deckstring = friendly_deckstring

        known_friendly_deck = deckstrings.Deck()
        known_friendly_deck.cards = convert(known_friendly_cards)
        known_friendly_deck.heroes = friendly_heroes
        known_friendly_deck.format = 2
        known_friendly_deckstring = known_friendly_deck.as_deckstring
        known_p1_deckstring = known_friendly_deckstring
    #except:
    #    p1_deckstring = ''
        
    #try:
    if True:
        opposing_cards = []
        known_opposing_cards = []
        if game_info['opposing_deck']['cards']: opposing_cards += game_info['opposing_deck']['cards']
        if game_info['opposing_deck']['cards']: known_opposing_cards += game_info['opposing_deck']['cards']
        if game_info['opposing_deck']['predicted_cards']: opposing_cards = game_info['opposing_deck']['predicted_cards']
        opposing_heroes = [card_id_to_dbfId[game_info['opposing_player']['hero_id']]]

        opposing_deck = deckstrings.Deck()
        opposing_deck.cards = convert(opposing_cards)
        opposing_deck.heroes = opposing_heroes
        opposing_deck.format = 2
        opposing_deckstring = opposing_deck.as_deckstring
        p2_deckstring = opposing_deckstring

        known_opposing_deck = deckstrings.Deck()
        known_opposing_deck.cards = convert(known_opposing_cards)
        known_opposing_deck.heroes = opposing_heroes
        known_opposing_deck.format = 2
        known_opposing_deckstring = known_opposing_deck.as_deckstring
        known_p2_deckstring = known_opposing_deckstring
    #except:
    #    p2_deckstring = ''
    if game_info['friendly_player']['player_id'] != 1:
        p1_deckstring, p2_deckstring = p2_deckstring, p1_deckstring
        known_p1_deckstring, known_p2_deckstring = known_p2_deckstring, known_p1_deckstring
        #cursor.execute("""INSERT INTO hsreplay.hsreplay_decks (game_id, p1_deck_code, p2_deck_code) VALUES ('%(game_id)s', '%(p1_deckstring)s', '%(p2_deckstring)s')""" % locals())
    #print(known_p2_deckstring, p2_deckstring, '\n', known_opposing_cards, opposing_cards, len(known_opposing_cards), len(opposing_cards))
    #assert False
    #cursor.execute("""UPDATE hsreplay.hsreplay_decks 
    #                  SET p1_deck_code = '%(p1_deckstring)s', p2_deck_code = '%(p2_deckstring)s',
    #                      known_p1_deck_code = '%(known_p1_deckstring)s', known_p2_deck_code = '%(known_p2_deckstring)s' 
    #                  WHERE game_id = '%(game_id)s'""" % locals())
    #connection.commit()
    cursor.execute("""UPDATE hsreplay.hsreplay_decks 
                      SET known_p1_deck_code = '%(known_p1_deckstring)s', known_p2_deck_code = '%(known_p2_deckstring)s' 
                      WHERE game_id = '%(game_id)s'""" % locals())
    connection.commit()


cursor.execute("SELECT game_id FROM hsreplay.hsreplay order by time")
game_ids = [i for (i,) in cursor.fetchall()]

#cursor.execute("SELECT game_id FROM hsreplay.hsreplay_decks WHERE known_p1_deck_code is not null")
#game_ids_decks = [i for (i,) in cursor.fetchall()]
game_ids_decks = []

to_update = [i for i in game_ids if i not in game_ids_decks]

total = len(to_update)
print("UPDATING:", len(to_update))

for game_id in to_update:
    check_update(game_id, total)
