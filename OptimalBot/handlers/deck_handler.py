import re
import sys
from arg_split import get_args
from deck_manager import EasyDeck, print_side_by_side, print_side_by_side_diff, side_by_side_diff_lines


class DeckHandler():
    def __init__(self):
            pass

    def handle(self, arguments, collectible=None):
        args = get_args(arguments)
        deckstrings = []
        flags = {}
        for i in args:
            if len(i) == 1:
                deckstrings.append(i[0])
            else:
                flags[i[0].replace('--', '')] = " ".join(i[1:])

        #deckstrings = arguments
        #deckstrings = deckstrings.split(' ')

        try:
            if len(deckstrings) == 1:
                return '`' + EasyDeck(deckstrings[0]).deck_print_lines() + '`'
            else:
                return '`' + side_by_side_diff_lines([EasyDeck(i) for i in deckstrings]) +'`'
        except:
            return '`%s`' % "Error: Bad deckstring"
