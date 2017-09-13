#!/usr/bin/python3
from __future__ import print_function
import re
from deck_manager import EasyDeck, print_side_by_side, print_side_by_side_diff
#from euPrelimsListUrls import deck_urls
#import requests
#from euDecklistCodesSummer import decks as decklistToAnalyze
#from apacDecklistCodesSummer import decks as decklistToAnalyze
from naDecklistCodesSummer import na_decks as decklistToAnalyze
from archetypes import get_archetypes_by_class
from archetype_labels import example_to_archetype, archetype_to_example

def getCodes(url):
    name = url.replace('https://www.icy-veins.com/hearthstone/', '').replace('-decks-at-hct-eu-summer-playoffs-2017', '')
    request = requests.get(url)
    content = request.content
    groups = re.findall("copyToClipboard\('\S+'\)", content)
    list_codes = [g.replace("copyToClipboard('", "").replace("')", "") for g in groups]
    return name, list_codes

decks = []
#for url in deck_urls:
#    name, lists = getCodes(url)
#    print(name)
#    for dl in lists:
#        decks.append(EasyDeck(dl, name))
#        print(dl)

class_lineups = {}
lineups = {}
for name, lists in decklistToAnalyze.items():
    #print(name)
    lu = []
    if name not in lineups:
        lineups[name] = []
    for dl in lists:
        deck = EasyDeck(dl, name)
        lineups[name].append(deck)
        decks.append(deck)
        lu.append(deck.get_class())
        #print(dl)
    lu = tuple(sorted(lu))
    class_lineups[lu] = class_lineups.get(lu, 0) + 1

deck_code_counts = {}
for deck in decks:
    code = deck.get_original_code()
    deck_code_counts[code] = deck_code_counts.get(code, 0) + 1

decks_by_class = {}
for deck in decks:
    deck_class = deck.get_class()
    if deck_class not in decks_by_class: 
        decks_by_class[deck_class] = []
    decks_by_class[deck_class].append(deck)

archetypes = get_archetypes_by_class(decks_by_class)

for deck_class in archetypes:
    archetypes[deck_class] = sorted(archetypes[deck_class], key=lambda x:len(x), reverse=True)

sample_archetypes = {}
for deck_class in archetypes:
    sample_archetypes[deck_class] = []
    for at in archetypes[deck_class]:
        sample_archetypes[deck_class].append(min([d for d in at], key=lambda x:x.get_average_distance(at)).get_copy(len(at)))

for deck_class in sorted(decks_by_class):
    print("  %-10s %s" % (deck_class, len(archetypes[deck_class])), [len(at) for at in archetypes[deck_class]])
    #if len(uncategorized_by_class[deck_class]) > 0:
    #    print deck_class, len(uncategorized_by_class[deck_class]), uncategorized_by_class[deck_class]

#for deck_class in sorted(decks_by_class):
#    print deck_class
#    print_side_by_side_diff([at[0] for at in sorted(archetypes[deck_class], key=lambda x:len(x), reverse=True)])
#print_side_by_side_diff([at[0] for at in sorted(archetypes['Mage'], key=lambda x:len(x), reverse=True)])
#print_side_by_side_diff([at[0] for at in sorted(archetypes['Priest'], key=lambda x:len(x), reverse=True)])
#print_side_by_side_diff([at[0] for at in sorted(archetypes['Warlock'], key=lambda x:len(x), reverse=True)])

arch_decks = {}
for arch_deck_list, name in example_to_archetype.items():
    arch_decks[name] = EasyDeck(arch_deck_list, name)

used_name = []
deck_to_archetype = {}
for deck_class in archetypes:
    for at in archetypes[deck_class]:
        label = "Unknown " + deck_class
        orig = "Unknown " + deck_class
        for name, arch_deck in arch_decks.items():
            if arch_deck.get_average_distance(at) <= 5:
                if name not in used_name:
                    label = name
                    #print(label)
                    used_name.append(label)
        if label == orig:
            problem_deck = at[0]
            #for name, arch_deck in arch_decks.items():
            #    if arch_deck.get_average_distance(at) <=5:
            #        label = name
            #print("DIST", deck_class, at_deck.deck.heroes, deck_class, arch_deck.get_average_distance(at), label)
            #print(arch_deck.get_original_code())
            #arch_deck.print_deck()
            print("DIST", deck_class, at_deck.deck.heroes, deck_class, problem_deck.get_average_distance(at), label)
            print(problem_deck.get_original_code())
            problem_deck.print_deck()
        for at_deck in at:
            deck_to_archetype[at_deck] = label

lineup_indexes = {}
for name, lu in lineups.items():
    lineup_set = set() 
    for deck in lu:
        lineup_set.add(deck_to_archetype[deck])
    index = tuple(sorted(lineup_set))
    if len(index) != 4:
        assert False, name
    lineup_indexes[index] = lineup_indexes.get(index, 0) + 1

#lineup_indexes = {}
#for lu in lineups.values():
#    lineup_set = set() 
#    for deck in lu:
#        dc = deck.get_class()
#        at_index = -1
#        for at in archetypes[dc]:
#            if deck in at:
#                #at_index = archetypes[dc].index(at)
#                at_index = at[0]
#        lineup_set.add((dc, at_index))
#    index = tuple(sorted(lineup_set))
#    lineup_indexes[index] = lineup_indexes.get(index, 0) + 1


res = ""
for name in "Deck 1,Deck 2,Deck 3,Deck4".split(','):
    res += "%-25s" % name
print("%85s" % str(res), "#")
for lu, count in sorted(lineup_indexes.items(), key = lambda x:x[1], reverse=True):
    res = ""
    for name in lu:
        res += "%-25s" % name
    #print("%85s" % str(res), count)
    print("%85s" % str(res), end = "")
    print(count)

# Find unique cards
card_info = {}
player_info = {}
for deck in decks:
    player = deck.name
    for card_id, count in deck.get_card_codes():
        if card_id not in card_info:
            card_info[card_id] = [0, []]
        card_info[card_id][0] += 1
        if player not in card_info[card_id][1]:
            card_info[card_id][1].append(player)
        

