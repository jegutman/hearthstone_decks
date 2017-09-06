import re
from deck_manager import EasyDeck, print_side_by_side, print_side_by_side_diff
#from euPrelimsListUrls import deck_urls
#import requests
#from euDecklistCodesSummer import decks as decklistToAnalyze
from apacDecklistCodesSummer import decks as decklistToAnalyze
from archetypes import get_archetypes_by_class

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

lineups = {}
for name, lists in decklistToAnalyze.items():
    #print(name)
    lu = []
    for dl in lists:
        deck = EasyDeck(dl, name)
        decks.append(deck)
        lu.append(deck.get_class())
        #print(dl)
    lu = tuple(sorted(lu))
    lineups[lu] = lineups.get(lu, 0) + 1

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

sample_archetypes = {}
for deck_class in archetypes:
    sample_archetypes[deck_class] = []
    for at in archetypes[deck_class]:
        sample_archetypes[deck_class].append(min([d for d in at], key=lambda x:x.get_average_distance(at)).get_copy(len(at)))

for deck_class in sorted(decks_by_class):
    print "  %-10s %s" % (deck_class, len(archetypes[deck_class])), [len(at) for at in archetypes[deck_class]]
    #if len(uncategorized_by_class[deck_class]) > 0:
    #    print deck_class, len(uncategorized_by_class[deck_class]), uncategorized_by_class[deck_class]

#for deck_class in sorted(decks_by_class):
#    print deck_class
#    print_side_by_side_diff([at[0] for at in sorted(archetypes[deck_class], key=lambda x:len(x), reverse=True)])
print_side_by_side_diff([at[0] for at in sorted(archetypes['Mage'], key=lambda x:len(x), reverse=True)])
print_side_by_side_diff([at[0] for at in sorted(archetypes['Priest'], key=lambda x:len(x), reverse=True)])
print_side_by_side_diff([at[0] for at in sorted(archetypes['Warlock'], key=lambda x:len(x), reverse=True)])
