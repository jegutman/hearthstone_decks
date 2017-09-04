import json
cards_file = open('cards.json')
cards_json = json.load(cards_file)

cards_by_id = {}
for card in cards_json:
    if 'dbfId' in card:
        cards_by_id[card['dbfId']] = card
