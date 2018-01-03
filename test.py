import re
from deck_manager import EasyDeck, print_side_by_side, print_side_by_side_diff
from apacDecklistCodesSummer import decks as decklistToAnalyze
from archetypes import get_archetypes_by_class
from archetype_labels import example_to_archetype, archetype_to_example

import sys

if sys.argv[1]:
    deck = EasyDeck(sys.argv[1])
else:
    deck = EasyDeck("AAECAf0ECMUE7QTtBewHuAi/CIivAtPFAguKAcABuwLJA6sEywSWBfsM17YCwcECmMQCAA==")
deck.print_deck()
print(deck.deck.heroes)
