from deck_manager import print_deck, deck_details, deck_from_string

from decks import decks

decklist = []
for name, code in decks:
    decklist.append((name, deck_from_string(code)))

def display_deck_comparison(decks):
    pass

def display_deck_comparison_from_strings(deckstrings):
    decks = [deck_from_string(ds) for ds in deckstrings]
    display_deck_comparison(decks)
