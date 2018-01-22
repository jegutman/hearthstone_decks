from json_win_rates import * 
from shared_utils import *
win_pcts, num_games, game_count, archetypes, overall_wr = get_win_pcts(min_game_threshold=0, min_game_count=0)

archetypes = [
    'Aggro Druid',
    'Jade Druid',
    #'Quest Druid', # Combo Druid
    'Aggro Hunter',
    'Secret Mage',
    'Big Spell Mage',
    #'Exodia Mage',
    'Tempo Rogue',
    #'Quest Rogue',
    'Aggro Paladin',
    #'Control Paladin',
    'Murloc Paladin',
    'Highlander Priest',
    'Dragon Priest',
    'Spiteful Priest',
    'Cube Warlock',
    'Demon Warlock',
    'Zoo Warlock',
    #'Pirate Warrior',
]
archetypes_2 = [
    'Aggro Druid',
    'Jade Druid',
    'Big Spell Mage',
    'Tempo Rogue',
    'Highlander Priest',
    'Cube Warlock',
    'Demon Warlock',
    #'Pirate Warrior',
]

diffs = {}

tmp_res = list(itertools.combinations(archetypes,2))
for i in tmp_res:
    a,b = i
    diffs[i] = similarity(a,b,win_pcts,archetypes_2)
