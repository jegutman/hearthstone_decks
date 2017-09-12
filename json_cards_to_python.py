import json
cards_file = open('cards.json')
cards_json = json.load(cards_file)

cards_by_id = {}
for card in cards_json:
    if 'dbfId' in card and 'set' in card and card.get('collectible', False) == True:
        cards_by_id[card['dbfId']] = card

card_name_to_id = {}
for card in cards_json:
    if 'dbfId' in card and 'set' in card and card.get('collectible', False) == True:
        card_name_to_id[card['name']] = card['dbfId']

names = {}
for card in cards_json:
    if 'dbfId' in card and 'name' in card and 'set' in card and card.get('collectible', False) == True:
        name = card['name']
        if name not in names:
            names[name] = []
        names[name].append(card['dbfId'])
