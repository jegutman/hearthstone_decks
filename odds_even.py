from json_cards_to_python import *

def odds(cardClass):
    res = []
    for i in all_cards_rotation:
        if i.get('cardClass') == cardClass and i.get('cost') and i.get('cost', 0) % 2 == 1:
            res.append(i)
    return res

def even(cardClass):
    res = []
    for i in all_cards_rotation:
        if i.get('cardClass') == cardClass and i.get('cost') and i.get('cost', 0) % 2 == 0:
            res.append(i)
    return res

def print_res(cards):
    for i in sorted(cards, key=lambda x:x.get('cost')):
        print("%2s %s" % (i.get('cost'), i.get('name')))
