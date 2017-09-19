import json
cards_file = open('cards.json')
cards_json = json.load(cards_file)

cards_by_id = {}
for card in cards_json:
    if 'dbfId' in card and 'set' in card and card.get('collectible', False):
        cards_by_id[card['dbfId']] = card

cards_by_raw_id = {}
for card in cards_json:
    #if 'id' in card and 'set' in card and card.get('collectible', False):
    cards_by_raw_id[card['id']] = card

card_name_to_id = {}
for card in cards_json:
    if 'dbfId' in card and 'set' in card and card.get('collectible', False):
        card_name_to_id[card['name']] = card['dbfId']

names = {}
for card in cards_json:
    if 'dbfId' in card and 'name' in card and 'set' in card and card.get('collectible', False) == True:
        name = card['name']
        if name not in names:
            names[name] = []
        names[name].append(card['dbfId'])

hero_powers = {}
for card in cards_json:
    if 'type' in card:
        if card['type'] == 'HERO_POWER':
            hero_powers[card['id']] = card

def lookup_card_name(card):
    if 'card_id' not in dir(card): return "Not Card"
    if card.card_id is None: return "Unknown Card"
    return cards_by_raw_id[card.card_id]['name']
