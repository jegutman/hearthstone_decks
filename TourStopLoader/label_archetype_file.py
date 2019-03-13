import sys
sys.path.append('../')
from config import basedir
sys.path.append(basedir)
sys.path.append(basedir + '/lineupSolver')
from json_cards_to_python import *
from deck_manager import *
from hearthstone import *

reference_decks = {}
file = open(basedir + '/TourStopLoader/hsreplay_archetypes.csv')
for line in file:
    card_class, archetype, deck_code = line.strip().split(',')
    reference_decks[card_class] = reference_decks.get(card_class, []) + [EasyDeck(deck_code, archetype)]

def label_archetype(code, threshold=8, reference_decks=reference_decks, default=None):
    DEBUG = True
    try:
        deck = EasyDeck(code)
    except:
        print('\n')
        print("Invalid Deck Code: %s" % code)
        print('\n')
        return None
    reference_class = deck.get_class().capitalize()
    try:
        distances = sorted([(d.get_distance(deck), d) for d in reference_decks[reference_class]], key=lambda x:x[0])
    except:
        print("Error", deck, reference_decks[reference_class])
        return None
    if distances[0][0] <= threshold:
        return distances[0][1].name
    else:
        lower_threshold = min(int(round(threshold / 30. *  len(deck.deck.cards) - 0.499999, 0)), 1)
        tmp_dists = [(deck.get_distance(d), d) for d in reference_decks[reference_class]]
        distances = sorted(tmp_dists, key=lambda x:x[0])
        if distances[0][0] <= lower_threshold:
            return distances[0][1].name
        if default is None:
            return 'Other ' + deck.get_class().capitalize()
        else:
            return default
