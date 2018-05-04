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

date = '2018_05_01'

def make_archetype_sheet(archetype):
    region = 'EU'
    output_file = open('EU_sheets/%(archetype)s.csv' % locals(), 'w')
    decks = []
    deckstrings = []
    cursor.execute("SELECT deck_name, deck_id, deck_code FROM deckstrings.decks WHERE deck_archetype = '%(archetype)s' and playoff_region = '%(region)s'" % locals())
    for deck_name, deck_id, deck_code in cursor.fetchall():
        deck_code = deck_code.strip()
        deckstrings.append(deck_code)
        decks.append(EasyDeck(deck_code, deck_name))

    compare = decks[0]
    for i in range(0, len(decks)):
        decks = decks[:i+1] + sorted(decks[i+1:], key=lambda x:x.get_distance(decks[i]))
    print(side_by_side_diff_csv(decks))
    print(len(set(deckstrings)), len(deckstrings))

make_archetype_sheet('Spiteful Druid')
