from __future__ import print_function
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
        return str(self.name) + ' ' + self.get_class() + ' ' + str(self.deckstring)

    def get_copy(self, new_name):
        return EasyDeck(self.deckstring, new_name)

    def get_print_lines(self): 
        res = [""]
        total = 0
        deck = []
        for i,j in self.deck.cards:
            total += j
            count, name, card_class, cost = j, cards[i]['name'], cards[i]['cardClass'], cards[i]['cost']
            if card_class == 'NEUTRAL':
                card_class = "ZZ_NEUTRAL"
            deck.append([card_class, cost, name, count])
        deck.sort()
        for card_class, cost, name, count in deck:
            res += ["%-2s %-25s x%s" % (cost, name, count)] 
        return res

    def get_cards_to_print(self): 
        res = {}
        for i,j in self.deck.cards:
            count, name, card_class, cost = j, cards[i]['name'], cards[i]['cardClass'], cards[i]['cost']
            if card_class == 'NEUTRAL':
                card_class = "ZZ_NEUTRAL"
            res[(card_class, i)] = j
        return res

    def deck_print_lines(self):
        res = "" + self.get_class() + '\n'
        total = 0
        deck = []
        for i,j in self.deck.cards:
            total += j
            count, name, card_class, cost, card_set = j, cards[i]['name'], cards[i]['cardClass'], cards[i]['cost'], cards[i]['set']
            if card_class == 'NEUTRAL':
                card_class = "ZZ_NEUTRAL"
            deck.append([card_class, cost, name, count, card_set])
        deck.sort(key=lambda x:x[1:])
        for card_class, cost, name, count, card_set in deck:
            res += "%-2s %-26s x%s %s" % (cost, name, count, card_set) + "\n"
        return res

    def print_deck(self):
        print(self.deck_print_lines())

    def get_distance(self, other_deck):
        s1 = self.card_set
        s2 = other_deck.card_set
        return len(s1.difference(s2))

    def get_average_distance(self, other_decks):
        total = sum([self.get_distance(od) for od in other_decks])
        return total / float(len(other_decks))

    def get_class(self):
        class_map = {
            274  : 'Druid',
            50484: 'Druid',
            671  : 'Paladin',
            2827 : 'Paladin',
            46116: 'Paladin',
            813  : 'Priest',
            41887: 'Priest',
            7    : 'Warrior',
            2828 : 'Warrior',
            1066 : 'Shaman',
            40183: 'Shaman',
            637  : 'Mage',
            2829 : 'Mage',
            39117: 'Mage',
            893  : 'Warlock',
            47817: 'Warlock',
            31   : 'Hunter',
            930  : 'Rogue',
            40195: 'Rogue',
        }
        return class_map[self.deck.heroes[0]]
    
    def get_original_code(self):
        return self.deckstring

    def get_card_codes(self):
        return self.deck.cards

    def get_card_set(self):
        return self.get_card_codes_long_set()

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

def print_side_by_side(list_of_decks):
    list_of_decks = sorted(list_of_decks, key=lambda x:x.get_distance(list_of_decks[0]))
    deck_print_lines = [d.get_print_lines() for d in list_of_decks]
    lengths = [len(dpl) for dpl in deck_print_lines]
    for dpl in deck_print_lines:
        if len(dpl) < max(lengths):
            dpl += [""] * (max(lengths) - len(dpl))
    for i in range(0, max(lengths)):
        for dpl in deck_print_lines:
            print("%35s" % dpl[i], end = "")
        print("")

def print_side_by_side_diff(list_of_decks):
    list_of_decks = sorted(list_of_decks, key=lambda x:x.get_distance(list_of_decks[0]))
    #get_cards_to_print
    deck_cards_to_print = [d.get_cards_to_print() for d in list_of_decks]
    for dl in list_of_decks:
        print("     %-20s     " % (dl.name), end = "")
    card_set = set()
    for cl in deck_cards_to_print:
        card_set = card_set.union(set(cl.keys()))
    #sorted_card_set = sorted(card_set, key=lambda x:(cards[x[1]]['cardClass'].replace('NEUTRAL', 'ZZ_NEUTRAL'), cards[x[1]]['cost'], cards[x[1]]['name']))
    # dont sort player class
    sorted_card_set = sorted(card_set, key=lambda x:(cards[x[1]]['cost'], cards[x[1]]['name']))
    for card_class, card_number in sorted_card_set:
        card_name = cards[card_number]['name']
        print("%-5s" % cards[card_number]['cost'], end = "")
        for dl in deck_cards_to_print:
            card_count = dl.get((card_class, card_number), 0)
            if card_count:
                print("%-25s x%1s  " % (card_name, card_count), end = "")
            else:
                print("%-25s  %1s  " % ("", ""), end = "")
        print("")

def side_by_side_diff_lines(list_of_decks):
    list_of_decks = sorted(list_of_decks, key=lambda x:x.get_distance(list_of_decks[0]))
    deck_cards_to_print = [d.get_cards_to_print() for d in list_of_decks]
    diffs = {}
    cost = {}
    res = ["" + list_of_decks[0].get_class()]
    card_set = set()
    for cl in deck_cards_to_print:
        card_set = card_set.union(set(cl.keys()))
    sorted_card_set = sorted(card_set, key=lambda x:(cards[x[1]]['cost'], cards[x[1]]['name']))
    for card_class, card_number in sorted_card_set:
        card_name = cards[card_number]['name']
        diffs[card_name] = 0
        cost[card_name] = cards[card_number]['cost']
        line = ""
        line += "%-5s" % cards[card_number]['cost']
        isFirst = True
        for dl in deck_cards_to_print:
            card_count_tmp = dl.get((card_class, card_number), 0)
            if card_count_tmp:
                card_count = "x%1s" % card_count_tmp
            else:
                card_count = "  "
            if isFirst:
                diffs[card_name] -= card_count_tmp
                line += "%-27s %2s  " % (card_name, card_count)
                isFirst = False
            else:
                diffs[card_name] += card_count_tmp
                line += " %2s  " % (card_count)
        res.append(line)
    res.append("")
    if len(list_of_decks) == 2:
        for card_name in sorted(diffs, key=lambda x:(diffs[x], cost[x])):
            if diffs[card_name] != 0:
                diff = diffs[card_name]
                if diff > 0:
                    diff = "+%s" % diff
                res.append("    %2s %s" % (diff, card_name))
    return '\n'.join(res)
