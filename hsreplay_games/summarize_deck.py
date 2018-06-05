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

sql = """SELECT game_id, date, time, p1, p2, p1_rank, p2_rank, archetype1, archetype2, num_turns, result, known_p1_deck_code, known_p2_deck_code
         FROM hsreplay.hsreplay join hsreplay.hsreplay_decks using(game_id)
         WHERE (p1 like '%(player_search)s' AND archetype1 like '%(archetype)s') or (p2 like '%(player_search)s' AND archetype2 like '%(archetype)s')
         ORDER BY time
"""

player_search  = sys.argv[1]
archetype = " ".join(sys.argv[2:])
cursor.execute(sql % locals())
total = 0
wins = 0
total_by_arch = {}
wins_by_arch = {}
decks = []
strings = []
for game_id, date, time, p1, p2, p1_rank, p2_rank, archetype1, archetype2, num_turns, result, known_p1_deck_code, known_p2_deck_code in cursor.fetchall():
    game_time = datetime.fromtimestamp(time - 3600 * 5)
    time_string = game_time.strftime("%H:%M:%S")
    game_id = game_id.strip()
    date = date.strip()
    p1 = p1.strip()
    p2 = p2.strip()
    p1_rank = p1_rank.strip()
    p2_rank = p2_rank.strip()
    archetype1 = archetype1.strip()
    archetype2 = archetype2.strip()
    result = result.strip()
    num_turns = int(num_turns)
    known_p1_deck_code = known_p1_deck_code.strip()
    known_p2_deck_code = known_p2_deck_code.strip()
    if not known_p1_deck_code: continue
    if p2.lower() == player_search.lower() or player_search.replace('%', '').lower() in p2.lower():
        p1, p2 = p2, p1
        p1_rank, p2_rank = p2_rank, p1_rank
        archetype1, archetype2 = archetype2, archetype1
        result = 'L' if result == 'W' else 'W'
        known_p1_deck_code, known_p2_deck_code = known_p2_deck_code, known_p1_deck_code

    print("found deck:", known_p1_deck_code)
    try:
        d = EasyDeck(known_p1_deck_code, debug=False)
        if d.card_count() == 30 and known_p1_deck_code not in strings:
            d.print_deck()
            strings.append(known_p1_deck_code)
        if d.get_class().capitalize() != archetype.split(' ')[-1]: continue
        decks.append(d)
    except:
        print("skipped")
        continue

cards = {}
for deck in decks:
    for card, qty in deck.deck.cards:
        cards[card] = max(cards.get(card, 0), qty)

res = {}
total = 0
for i,j in cards.items():
    count, name, card_class, cost = j, cards_by_id[i]['name'], cards_by_id[i]['cardClass'], cards_by_id[i]['cost']
    if card_class == 'NEUTRAL':
        card_class = "ZZ_NEUTRAL"
    res[(cost, name)] = j
    total += j


for i,j in sorted(res.items()):
    a, b = i
    print("%2s %-25s %s" % (a,b, j))
print("total:", total)
#friendly_deck = deckstrings.Deck()
#friendly_deck.cards = convert(friendly_cards)
#friendly_deck.heroes = friendly_heroes
#friendly_deck.format = 2
#friendly_deckstring = friendly_deck.as_deckstring
#p1_deckstring = friendly_deckstring
