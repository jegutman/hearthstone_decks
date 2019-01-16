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

def make_archetype_sheet(archetype):
    archetype_print = archetype.replace(' ', '')
    region = 'NA'
    output_file = open('NA_sheets/%(archetype_print)s.csv' % locals(), 'w')
    decks = []
    deckstrings = []
    cursor.execute('SELECT deck_name, deck_id, deck_code FROM deckstrings.decks WHERE deck_archetype = "%(archetype)s" and playoff_region = "%(region)s" and date > "2019_01_01"' % locals())
    for deck_name, deck_id, deck_code in cursor.fetchall():
        deck_code = deck_code.strip()
        deckstrings.append(deck_code)
        decks.append(EasyDeck(deck_code, deck_name))

    compare = decks[0]
    for i in range(0, len(decks)):
        decks = decks[:i+1] + sorted(decks[i+1:], key=lambda x:x.get_distance(decks[i]))
    output_file.write(side_by_side_diff_csv(decks))
    output_file.close()
    #print(len(set(deckstrings)), len(deckstrings))

def make_lineups_sheet():
    output_file = open('NA_sheets/Lineups.csv', 'w')
    region = 'NA'
    cursor.execute("SELECT deck_name, deck_archetype FROM deckstrings.decks WHERE playoff_region = '%(region)s' and date > '2019_01_01'" % locals())
    player_decks = {}
    output_file.write("Player,Deck1,Deck2,Deck3,Deck4\n")
    for deck_name, deck_archetype in cursor.fetchall():
        if deck_name not in player_decks:
            player_decks[deck_name] = []
        player_decks[deck_name].append('"' + deck_archetype + '"')

    for i in player_decks:
        player_decks[i].sort(key=lambda x:x.split(' ')[-1])

    lineups = {}
    for i, j in sorted(player_decks.items(), key=lambda x:x[0].lower()):
        lineups[tuple(j)] = lineups.get(tuple(j), []) + [i]
        output_file.write('"' + i + '",')
        output_file.write(",".join(j))
        output_file.write("\n")
    output_file.write('\n\n')
    num_players = len(player_decks.keys())
    output_file.write("Deck1,Deck2,Deck3,Deck4,Percent of Field,,Players\n")
    for lu, players in sorted(lineups.items(), key=lambda x:len(x[1]), reverse=True):
        output_file.write(",".join(list(lu)) + "," + str(round(len(players) / float(num_players) * 100, 1)) + ",," + ",".join(players) + '\n')

def archetype_percents():
    output_file = open('NA_sheets/Archetypes.csv', 'w')
    output_file.write("Archetype,Number,Percentage of Decks\n")
    region = 'NA'
    total = 0
    cursor.execute("select deck_archetype, deck_class, count(deck_archetype) as total FROM deckstrings.decks WHERE playoff_region = '%(region)s' and date > '2019_01_01' group by deck_archetype, deck_class order by deck_class, total desc" % locals())
    archetypes = []
    for i,j,k in cursor.fetchall():
        i = '"' + i + '"'
        k = int(k)
        archetypes.append((i,k))
        total += k
    for i,j in archetypes:
        output_file.write(",".join([i, str(j), str(round(j/float(total) * 100, 1))]) + '\n')

archetype_percents()
    

make_lineups_sheet()

region = 'NA'
cursor.execute("SELECT distinct deck_archetype FROM deckstrings.decks WHERE playoff_region = '%(region)s' and date > '2019_01_01'" % locals())
for (archetype,) in cursor.fetchall():
    make_archetype_sheet(archetype)


