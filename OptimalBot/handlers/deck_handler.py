import re

import sys
sys.path
#sys.path.append('/Users/jgutman/workspace/hearthstone_decks')
sys.path.append('/root/workspace/hearthstone_decks')
from deck_manager import EasyDeck, print_side_by_side, print_side_by_side_diff, side_by_side_diff_lines


class DeckHandler():
	def __init__(self):
            pass

	def handle(self, deckstrings, collectible=None):
            try:
                deckstrings = deckstrings.split(' ')
                if len(deckstrings) == 1:
                    return '`' + EasyDeck(deckstrings[0]).deck_print_lines() + '`'
                else:
                    return '`' + side_by_side_diff_lines([EasyDeck(i) for i in deckstrings]) +'`'
            except:
                return '`%s`' % "Error: Bad deckstring"
