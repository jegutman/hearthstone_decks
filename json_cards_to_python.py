import json
from config import *
cards_file = open(basedir + 'cards.json')
cards_json = json.load(cards_file)

cards_by_id = {}
all_cards_by_id = {}
for card in cards_json:
    #if 'dbfId' in card and 'set' in card and card.get('collectible', False):
    if 'dbfId' in card and card.get('collectible', False):
        cards_by_id[card['dbfId']] = card
    if 'dbfId' in card:
        all_cards_by_id[card['dbfId']] = card

card_id_to_dbfId = {}
for card in cards_json:
    #if 'dbfId' in card and 'set' in card and card.get('collectible', False):
    if 'dbfId' in card and card.get('collectible', False):
        card_id_to_dbfId[card['id']] = card['dbfId']

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


standard_sets = [
    'ICECROWN', 
    'CORE', 
    'EXPERT1', 
    'UNGORO', 
    'LOOTAPALOOZA',
    'GILNEAS',
    'BOOMSDAY',
    'TROLL',
]

rotation_sets = [
    'CORE', 
    'EXPERT1', 
    'GILNEAS',
    'BOOMSDAY',
    'TROLL',
]

wild_sets = [
    'LOE', 
    'TGT', 
    'BRM', 
    'GVG', 
    'NAXX',
    'HOF', 
    ]

all_sets = standard_sets + wild_sets

all_cards_standard = []
all_cards_wild = []
all_cards_rotation = []
for card in cards_json:
    if 'dbfId' in card and 'set' in card and card.get('collectible', False) and card['set'] in standard_sets:
        all_cards_standard.append(card)
    if 'dbfId' in card and 'set' in card and card.get('collectible', False) and card['set'] in rotation_sets:
        all_cards_rotation.append(card)
    if 'dbfId' in card and 'set' in card and card.get('collectible', False):
        all_cards_wild.append(card)

def get_cards_by_cost(cost, useStandard=True, minions_only=True):
    fullset = all_cards_standard if useStandard else all_cards_wild
    if minions_only:
        return [c for c in fullset if c.get('cost', -1) == cost and c.get('type') == 'MINION']
    else:
        return [c for c in fullset if c.get('cost', -1) == cost]

def get_cards_filtered(cost=None, class_filter=None, card_set=None, minions_only=False):
    if card_set is None:
        fullset = all_cards_standard
    else:
        fullset = card_set
    res_tmp = [c for c in fullset]
    if cost:
        res_tmp = [c for c in res_tmp if c.get('cost') == cost]
    if minions_only:
        res_tmp = [c for c in res_tmp if c.get('type') == 'MINION']
    if class_filter:
        res_tmp = [c for c in res_tmp if c.get('cardClass') in class_filter]
    return res_tmp


def get_minions_by_attack(attack, useStandard=True):
    fullset = all_cards_standard if useStandard else all_cards_wild
    return sorted([c for c in fullset if c.get('attack', -1) == attack and c.get('type') == 'MINION'], key=lambda x:x.get('cost'))

def get_average_stats(cost, useStandard=True):
    test_set = get_cards_by_cost(cost, useStandard)
    attack, health, count = 0,0, 0
    for i in test_set:
        if i.get('type') == 'MINION':
            attack += i.get('attack')
            health += i.get('health')
            count += 1
    return (round(attack / float(count), 2), round(health / float(count), 2), count)
