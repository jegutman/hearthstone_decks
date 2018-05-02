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
region = 'EU'

archetype = " ".join(sys.argv[1:])

cursor.execute("SELECT deck_name, deck_archetype FROM deckstrings.playoffs" % locals())
player_decks = {}
for deck_name, deck_archetype in cursor.fetchall():
    if deck_name not in player_decks:
        player_decks[deck_name] = []
    player_decks[deck_name].append(deck_archetype)

for i in player_decks:
    player_decks[i].sort(key=lambda x:x.split(' ')[-1])

lineups = {}
for i, j in player_decks.items():
    j = tuple(j)
    if j not in lineups: lineups[j] = []
    lineups[j].append(i)

#for i,j in sorted(lineups.items(), key=lambda x:len(x[1]), reverse=True):
#    #print(len(j), i)
#    print(",".join(list(i)), end="")
#    print(',' + " ".join(list(j)))

for i,j in sorted(lineups.items(), key=lambda x:len(x[1]), reverse=True):
    print('"' + ",".join(list(i)) + '"')

lens = []
for i,j in sorted(lineups.items(), key=lambda x:len(x[1]), reverse=True):
    lens.append(str(len(j)))
print(",".join(lens))
