import re
from deck_manager import EasyDeck, print_side_by_side, print_side_by_side_diff
from apacDecklistCodesSummer import decks as decklistToAnalyze
from archetypes import get_archetypes_by_class
from archetype_labels import example_to_archetype, archetype_to_example

import sys

decks = []
copa = open('Decklists_Copa.csv')
count = 0
name = sys.argv[1]
for line in copa:
    tmp = line.split(',')
    if name in tmp[0]:
        for i in tmp[2:]:
            EasyDeck(i).print_deck()
        
#decks.append(EasyDeck(deckstring))
#print_side_by_side_diff(decks)
