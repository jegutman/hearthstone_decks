import requests
import re
from deck_manager import EasyDeck, print_deck, deck_details, deck_from_string
from euPrelimsListUrls import deck_urls

def getCodes(url):
    name = url.replace('https://www.icy-veins.com/hearthstone/', '').replace('-decks-at-hct-eu-summer-playoffs-2017', '')
    request = requests.get(url)
    content = request.content
    groups = re.findall("copyToClipboard\('\S+'\)", content)
    list_codes = [g.replace("copyToClipboard('", "").replace("')", "") for g in groups]
    return name, list_codes

decks = []
for url in deck_urls:
    name, lists = getCodes(url)
    print(name)
    for dl in lists:
        decks.append(EasyDeck(dl, name))
        print(dl)

deck_code_counts = {}
for deck in decks:
    code = deck.get_original_code()
    deck_code_counts[code] = deck_code_counts.get(code, 0) + 1
