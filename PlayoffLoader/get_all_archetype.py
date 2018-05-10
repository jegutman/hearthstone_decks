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
region = 'NA'

archetype = " ".join(sys.argv[1:])

decks = []
deckstrings = []
#cursor.execute("SELECT deck_name, deck_id, deck_code FROM deckstrings.playoffs WHERE deck_archetype = '%(archetype)s' and deck_name in ('ThijsNL#2223', 'Rdu#2340', 'Leta#21458', 'Hypno#22145', 'anduriel#21364')" % locals())
cursor.execute("SELECT deck_name, deck_id, deck_code FROM deckstrings.decks WHERE playoff_region = 'NA' and deck_archetype = '%(archetype)s'" % locals())
#print("SELECT deck_name, deck_id, deck_code FROM deckstrings.playoffs WHERE deck_archetype = '%(archetype)s'" % locals())
for deck_name, deck_id, deck_code in cursor.fetchall():
    #print(deck_name, deck_id, deck_code)
    deck_code = deck_code.strip()
    deckstrings.append(deck_code)
    decks.append(EasyDeck(deck_code, deck_name))

compare = decks[0]
for i in range(0, len(decks)):
    decks = decks[:i+1] + sorted(decks[i+1:], key=lambda x:x.get_distance(decks[i]))
print(side_by_side_diff_lines(decks))
print(len(set(deckstrings)), len(deckstrings))
