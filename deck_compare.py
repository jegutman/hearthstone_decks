from deck_manager import print_deck, deck_details, deck_from_string

from decks import decks

decklist = []
for name, code in decks:
    decklist.append((name, deck_from_string(code)))
