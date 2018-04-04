import re

import sys
sys.path
#sys.path.append('/Users/jgutman/workspace/hearthstone_decks')
sys.path.append('/root/workspace/hearthstone_decks')
from deck_manager import EasyDeck, print_side_by_side, print_side_by_side_diff


class DeckHandler():
	def __init__(self):
            pass

	def handle(self, input, collectible=None):
            return '`' + EasyDeck(input).deck_print_lines() + '`'
