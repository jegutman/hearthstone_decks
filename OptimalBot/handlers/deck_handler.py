from shared_utils import *
from config import *
import re
import sys
from arg_split import get_args
from deck_manager import EasyDeck, print_side_by_side, print_side_by_side_diff, side_by_side_diff_lines

helpstring = """`Deck:
To insert a deck: !deck <deckstring> --name <deck_name> --archetype <archetype>
    (name and archetype flags are optional, but helpful)
To update a deck: !update <deckstring> --name <deck_name> --archetype <archetype>
`
"""

helpstring_search = """`Search:
Flags that can be used for search:
-name
-class
-archetype
-date (format YYYY_MM_DD)
all of these accept .* as a wildcard
`
"""

class DeckHandler():
    def __init__(self):
        pass

    def handle(self, args, message, deck_db_handler):
        if 'help' in args.split(' ')[0]:
            return helpstring
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

    def handle_search(self, args, message, deck_db_handler):
        deckstrings, flags = get_args(args)
        if 'help' in args.split(' ')[0]:
            return helpstring_search
        if message.channel.name in PRIVATE_CHANNELS or message.server.name in PRIVATE_SERVERS:
            allow_private = True
        else:
            allow_private = False
        return deck_db_handler.search(args,flags, allow_private)
        
