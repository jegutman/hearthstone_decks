from hearthstone.deckstrings import Deck
from hearthstone.enums import FormatType
import json
import sys
from json_cards_to_python import cards_by_id as cards

class EasyDeck():
    self.deck = None

    def __init__(self, deckstring):
        self.deck = Deck.from_deckstring(deck_string)

    def __repr__(self):
        res = ""
        total = 0
        deck = []
        for i,j in deck_cards:
            total += j
            count, name, card_class, cost = j, cards[i]['name'], cards[i]['playerClass'], cards[i]['cost']
            if card_class == 'NEUTRAL':
                card_class = "ZZ_NEUTRAL"
            deck.append([card_class, cost, name, count])
        deck.sort()
        last_class = ""
        for card_class, cost, name, count in deck:
            if card_class != last_class:
                res += ""
                res += card_class.replace('ZZ_', '')
            last_class = card_class
            res += "%-2s %-25s x%s" % (cost, name, count)

def print_deck(deck_cards, cards=cards):
    total = 0
    deck = []
    for i,j in deck_cards:
        total += j
        count, name, card_class, cost = j, cards[i]['name'], cards[i]['playerClass'], cards[i]['cost']
        if card_class == 'NEUTRAL':
            card_class = "ZZ_NEUTRAL"
        deck.append([card_class, cost, name, count])
    deck.sort()
    last_class = ""
    print("")
    for card_class, cost, name, count in deck:
        if card_class != last_class:
            print("")
            print(card_class.replace('ZZ_', ''))
        last_class = card_class
        print("%-2s %-25s x%s" % (cost, name, count))

def deck_details(deck_cards, cards=cards):
    total = 0
    deck = []
    for i,j in deck_cards:
        total += j
        count, name, card_class, cost = j, cards[i]['name'], cards[i]['playerClass'], cards[i]['cost']
        if card_class == 'NEUTRAL':
            card_class = "ZZ_NEUTRAL"
        deck.append([card_class, cost, name, count])
    deck.sort()
    return deck

def deck_from_string(deck_string):
    deck = Deck.from_deckstring(deck_string)
    return deck
