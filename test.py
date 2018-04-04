import re
from deck_manager import EasyDeck, print_side_by_side, print_side_by_side_diff
from apacDecklistCodesSummer import decks as decklistToAnalyze
from archetypes import get_archetypes_by_class
from archetype_labels import example_to_archetype, archetype_to_example

import sys

decks = []
for deckstring in sys.argv[1:]:
    decks.append(EasyDeck(deckstring))
if len(decks) > 1:
    print_side_by_side_diff(decks)
else:
    decks[0].print_deck()
