from hearthstone.deckstrings import Deck
from hearthstone.enums import FormatType
import json
import sys
from json_cards_to_python import cards_by_id as cards

def print_deck(deck_cards, cards):
    total = 0
    deck = []
    for i,j in deck_cards:
        total += j
        count, name, card_class, cost = j, cards[i]['name'], cards[i]['playerClass'], cards[i]['cost']
        if card_class == 'NEUTRAL':
            card_class = "ZZ_NEUTRAL"
        deck.append([card_class, cost, name, count])
        #print "%2s %1s %s %s %s" % (total, j, cards[i]['name'], cards[i]['playerClass'], cards[i]['cost'])
    deck.sort()
    last_class = ""
    print ""
    for card_class, cost, name, count in deck:
        if card_class != last_class:
            print ""
            print card_class.replace('ZZ_', '')
        last_class = card_class
        print "%-2s %-25s x%s" % (cost, name, count)

# Create a deck from a deckstring
deck = Deck()
deck.heroes = [7]  # Garrosh Hellscream
deck.format = FormatType.FT_WILD
# Nonsense cards, but the deckstring doesn't validate.
deck.cards = [(1, 3), (2, 3), (3, 3), (4, 3)]  # id, count pairs
#print(deck.as_deckstring)  # "AAEBAQcAAAQBAwIDAwMEAw=="

# Import a deck from a deckstring
#deck = Deck.from_deckstring("AAECAZ/HAh4JigH7AZcCnAK0AuUE7QXJBqUJ0wrVCtcK8gz7DKGsAoO7ArW7Are7Ati7Aui/Auq/Avq/AtHBAtjBAtnBAsrDAr7IAvDPApDTAgAA")
deck = Deck.from_deckstring(sys.argv[1])

print_deck(deck.cards, cards)
