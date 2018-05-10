import MySQLdb
import sys
sys.path.append('../')
from config import basedir
sys.path.append(basedir)
sys.path.append(basedir + '/lineupSolver')


from config import *
from shared_utils import *
from deck_manager import *
from json_cards_to_python import *
connection = MySQLdb.connect(host='localhost', user=db_user, passwd=db_passwd)
cursor = connection.cursor()

query = """
SELECT card_name, deck_class, card_id, sum(quantity) as total
FROM deckstrings.deck_to_cards join deckstrings.dbfid_to_card on card_id = dbfId join deckstrings.decks using(deck_id) 
WHERE user = 'NA Playoffs loader'
GROUP BY card_name, card_id, deck_class
ORDER BY total desc
"""

cursor.execute(query % locals())
for card_name, deck_class, card_id, total in cursor.fetchall():
    card = cards_by_id[card_id]
    line = [card_name, total, deck_class, card.get('cardClass'), card.get('rarity'), card.get('set')]
    print(",".join([str(i) for i in line]))
    #print("%-25s %s" % (card_name, total))
