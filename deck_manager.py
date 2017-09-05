from hearthstone.deckstrings import Deck
from hearthstone.enums import FormatType
import json
import sys
from json_cards_to_python import cards_by_id as cards

class EasyDeck():

    def __init__(self, deckstring, name = ""):
        self.deck = Deck.from_deckstring(deckstring)
        self.name = name
        self.deckstring = deckstring
        self.card_set = self.get_card_codes_long_set()
        assert sum([c[1] for c in self.deck.cards]) == 30, self.deck.cards

    def __repr__(self):
        return self.name + ' ' + self.get_class() + ' ' + self.deckstring
        

    def print_deck(self):
        res = ""
        total = 0
        deck = []
        for i,j in self.deck.cards:
            total += j
            count, name, card_class, cost = j, cards[i]['name'], cards[i]['playerClass'], cards[i]['cost']
            if card_class == 'NEUTRAL':
                card_class = "ZZ_NEUTRAL"
            deck.append([card_class, cost, name, count])
        deck.sort()
        last_class = ""
        for card_class, cost, name, count in deck:
            if card_class != last_class:
                res += "\n"
                res += card_class.replace('ZZ_', '') + "\n"
            last_class = card_class
            res += "%-2s %-25s x%s" % (cost, name, count) + "\n"
        print res

    def get_distance(self, other_deck):
        s1 = self.card_set
        s2 = other_deck.card_set
        return len(s1.difference(s2))

    def get_class(self):
        class_map = {
            274  : 'Druid',
            671  : 'Paladin',
            813  : 'Priest',
            7    : 'Warrior',
            1066 : 'Shaman',
            637  : 'Mage',
            893  : 'Warlock',
            31   : 'Hunter',
            930  : 'Rogue',
        }
        return class_map[self.deck.heroes[0]]
    
    def get_original_code(self):
        return self.deckstring

    def get_card_codes(self):
        return self.deck.cards

    def get_card_codes_long_set(self):
        res = set()
        for card in self.deck.cards:
            res.add(card[0])
            if card[1] == 2:
                res.add((card[0], "two"))
        return res

    def get_card_names(self):
        res = []
        for i, j in self.deck.cards:
            res.append((j, cards[i]))
        return res

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
