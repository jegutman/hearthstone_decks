import re
import sys
from arg_split import get_args
from deck_manager import EasyDeck, print_side_by_side, print_side_by_side_diff, side_by_side_diff_lines


class DeckHandler():
    def __init__(self):
            pass

    def handle(self, args, message, deck_db_handler):
        deckstrings, flags = get_args(args)
        if len(deckstrings) == 1:
            deck_code = deckstrings[0]
            deck_name = flags.get('name')
            deck_archetype = flags.get('archetype')
            deck_db_handler.process_deck(message, deck_code, name=deck_name, archetype=deck_archetype)
            try:
                return '`' + EasyDeck(deckstrings[0]).deck_print_lines() + '`'
            except:
                return '`%s`' % "Error: Bad deckstring"
        else:
            try:
                return '`' + side_by_side_diff_lines([EasyDeck(i) for i in deckstrings]) +'`'
            except:
                return '`%s`' % "Error: Bad deckstring"
    
    def handle_update(self, args, message, deck_db_handler):
        deckstrings, flags = get_args(args)
        deck_code = deckstrings[0]
        deck_name = flags.get('name')
        deck_archetype = flags.get('archetype')
        if deck_db_handler.update_deck_label(message, deck_code, name=deck_name, archetype=deck_archetype):
            return '`SUCCESS`'
        else:
            return '`UPDATE FAILED`'
        
