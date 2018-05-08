import MySQLdb
import sys
sys.path.append('../')
from config import basedir
sys.path.append(basedir)
sys.path.append(basedir + '/lineupSolver')


from config import *
from shared_utils import *
from deck_manager import *
connection = MySQLdb.connect(host='localhost', user=db_user, passwd=db_passwd)
cursor = connection.cursor()

filename = 'lineupSolver/2018_HCT_Europe_Summer_Playoffs.csv'

file = open(filename)

for line in file:
    deck_name, deck_class, deck_code = line.strip().split(',')
    #print(deck_name, deck_class, deck_code)
    deck_class = deck_class.capitalize()
    deck = EasyDeck(deck_code)
    deck_class = deck.get_class()
    max_results = flags.get('limit', 5)
    max_dist = flags.get('max_dist', 5)
    to_compare = get_decks_by_class(deck_class)
    res = []
    for deck_id, deck_archetype, deck_code_tmp in to_compare:
        tmp_deck = EasyDeck(deck_code_tmp)
        distance = deck.get_distance(tmp_deck)
        res.append((distance, deck_id, deck_archetype, deck_code_tmp))
    res_final = sorted([i for i in res if i[0] <= max_dist][:max_results])
    if len(res_final) == 0:
        print('No deck within %(max_dist)s cards of deck' % locals())
        print("%-25s %-10s %s" % (deck_name, deck_class, deck_code))
    else:
        print("%-25s %-10s %-15s %2s %s" % (deck_name, deck_class, res_final[0][2], res_final[0][0], deck_code))
        deck_archetype = res_final[0][2]
        cursor.execute("UPDATE deckstrings.playoffs set deck_archetype = '%(deck_archetype)s' WHERE deck_code = '%(deck_code)s'" % locals())

connection.commit()
