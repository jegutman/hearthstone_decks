import re
from deck_manager import EasyDeck, print_side_by_side, print_side_by_side_diff, side_by_side_diff_lines
from apacDecklistCodesSummer import decks as decklistToAnalyze
from archetypes import get_archetypes_by_class
from archetype_labels import example_to_archetype, archetype_to_example

import sys

decks = []
print("")
for deckstring in sys.argv[1:]:
    decks.append(EasyDeck(deckstring))
if len(decks) > 1:
    print(side_by_side_diff_lines(decks))
else:
    decks[0].print_deck()
