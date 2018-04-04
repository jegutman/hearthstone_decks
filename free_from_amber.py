from json_cards_to_python import *

free_from_amber = []

for x in range(8,30):
    for i in get_cards_by_cost(x):
      if i.get('cardClass') in ['NEUTRAL', 'PRIEST']:
        free_from_amber.append(i)
