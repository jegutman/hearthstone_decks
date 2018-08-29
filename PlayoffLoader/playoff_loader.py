import MySQLdb
import sys
sys.path.append('../')
from config import basedir
sys.path.append(basedir)
sys.path.append(basedir + '/lineupSolver')

import datetime


from config import *
from shared_utils import *
from deck_manager import *
connection = MySQLdb.connect(host='localhost', user=db_user, passwd=db_passwd)
cursor = connection.cursor()

from label_archetype import label_archetype

date = '2018_08_29'
region = 'EU'

deck_id = None

def process_deck(deck_code, deck_class, name, archetype, deck_id=None):
    deck_id += 1
    db, table = 'deckstrings,decks'.split(',')

    deck_code      = deck_code
    time           = datetime.datetime.now().strftime('%s')
    date           = datetime.datetime.now().strftime('%Y_%m_%d')
    server         = 'EU Playoffs Loader'
    user           = 'EU Playoffs Loader'
    is_private     = 0

    deck = EasyDeck(deck_code)
    
    #return insert_deck(deck, time, date, server, user, is_private, deck_code, deck_class, deck_archetype, deck_name, deck_id=deck_id)
    return insert_deck(deck, time, date, server, user, is_private, deck_code, deck_class, deck_archetype, deck_name)

def insert_cards(deck, deck_id):
    db = 'deckstrings'
    try:
        for card_id, quantity in deck.deck.cards:
            cursor.execute("INSERT INTO %(db)s.deck_to_cards (deck_id, card_id, quantity) VALUES (%(deck_id)s, %(card_id)s, %(quantity)s)" % locals())
        connection.commit()
    except:
        return False
    return True

def insert_deck(deck, time, date, server, user, is_private, deck_code, deck_class, deck_archetype = None, deck_name = None):
    db = 'deckstrings'
    playoff_region = 'EU'
    if deck_archetype: 
        deck_archetype = "'%s'" % deck_archetype
    else:
        deck_archetype = 'null'
    if deck_name: 
        deck_name = "'%s'" % deck_name
    else:
        deck_name = 'null'
    cursor.execute("""INSERT INTO %(db)s.decks (time, date, server, user, is_private, deck_code, deck_class, deck_archetype, deck_name, playoff_region)
                           VALUES (%(time)s, '%(date)s', '%(server)s', '%(user)s', %(is_private)s, '%(deck_code)s', '%(deck_class)s', %(deck_archetype)s, %(deck_name)s, '%(playoff_region)s')""" % locals())
    connection.commit()
    try:
        cursor.execute("SELECT deck_id FROM %(db)s.decks WHERE deck_code = '%(deck_code)s'" % locals())
        deck_id = cursor.fetchone()[0]
    except:
        return False
    try:
        cursor.execute("INSERT INTO %(db)s.deck_ids (deck_id, deck_code) VALUES (%(deck_id)s, '%(deck_code)s')" % locals())
        connection.commit()
    except:
        return False
    insert_cards(deck, deck_id)
    return True

#def insert_deck(deck, time, date, server, user, is_private, deck_code, deck_class, deck_archetype, deck_name, deck_id=None):
#    db = 'deckstrings'
#    deck_archetype = "'%s'" % deck_archetype
#    deck_name = "'%s'" % deck_name
#    playoff_region = 'EU'
#    if deck_id:
#        print("""INSERT INTO %(db)s.decks (deck_id, time, date, server, user, is_private, deck_code, deck_class, deck_archetype, deck_name, playoff_region)
#                               VALUES (%(deck_id)s, %(time)s, '%(date)s', '%(server)s', '%(user)s', %(is_private)s, '%(deck_code)s', '%(deck_class)s', %(deck_archetype)s, %(deck_name)s, '%(playoff_region)s')""" % locals())
##        cursor.execute("""INSERT INTO %(db)s.decks (deck_id, time, date, server, user, is_private, deck_code, deck_class, deck_archetype, deck_name, playoff_region)
#                               VALUES (%(deck_id)s, %(time)s, '%(date)s', '%(server)s', '%(user)s', %(is_private)s, '%(deck_code)s', '%(deck_class)s', %(deck_archetype)s, %(deck_name)s, '%(playoff_region)s')""" % locals())
#    else:
#        cursor.execute("""INSERT INTO %(db)s.decks ( time, date, server, user, is_private, deck_code, deck_class, deck_archetype, deck_name, playoff_region)
#                               VALUES (%(time)s, '%(date)s', '%(server)s', '%(user)s', %(is_private)s, '%(deck_code)s', '%(deck_class)s', %(deck_archetype)s, %(deck_name)s, '%(playoff_region)s')""" % locals())
#    connection.commit()
##    cursor.execute("SELECT deck_id FROM %(db)s.decks WHERE deck_code = '%(deck_code)s' and time = %(time)s" % locals())
#    connection.commit()
#    deck_id_tmp = cursor.fetchone()[0]
#    cursor.execute("INSERT INTO %(db)s.deck_ids (deck_id, deck_code) VALUES (%(deck_id_tmp)s, '%(deck_code)s')" % locals())
#    connection.commit()
#    insert_cards(deck, deck_id_tmp)
#    return True
#
#def insert_cards(deck, deck_id_tmp):
#    db = 'deckstrings'
#    for card_id, quantity in deck.deck.cards:
#        cursor.execute("INSERT INTO %(db)s.deck_to_cards (deck_id, card_id, quantity) VALUES (%(deck_id_tmp)s, %(card_id)s, %(quantity)s)" % locals())
#    connection.commit()
#    return True

###+---------+------------+--------+--------------+----------------+------------+----------------------------------------------------------------------------------+
###| deck_id | date       | region | deck_name    | deck_archetype | deck_class | deck_code                                                                        |
###+---------+------------+--------+--------------+----------------+------------+----------------------------------------------------------------------------------+
###|     385 | 2018_05_01 | EU     | Mryagut#2306 | Taunt Druid    | Druid      | AAECAbSKAwiQB4fOAsLOAq/TAubTAvHqAt3rAr/yAgtAX+kB5AjJxwKU0gKY0gKe0gKL4QKE5gKN8AIA |
###+---------+------------+--------+--------------+----------------+------------+----------------------------------------------------------------------------------+


#cursor.execute("SELECT deck_name, deck_archetype, deck_class, deck_code FROM deckstrings.playoffs")
filename = 'hct_europe_fall_decklists.csv'

file = open(filename)

flags = {}

def get_decks_by_class(deck_class):
    db, table = 'deckstrings,decks'.split(',')

    cursor.execute("SELECT deck_id, deck_archetype, deck_code FROM %(db)s.%(table)s WHERE deck_class = '%(deck_class)s' and deck_archetype is not null" % locals())
    return [(i,j,k) for (i,j,k) in cursor.fetchall()]

for line in file:
    deck_name, deck_class, deck_code = line.strip().split(',')
    #print(deck_name, deck_class, deck_code)
    deck_class = deck_class.capitalize()
    deck = EasyDeck(deck_code)
    deck_class = deck.get_class()
    max_results = flags.get('limit', 5)
    max_dist = flags.get('max_dist', 5)
    deck_archetype = label_archetype(deck, threshold=8)
    process_deck(deck_code, deck_class, deck_name, deck_archetype, deck_id=deck_id)
