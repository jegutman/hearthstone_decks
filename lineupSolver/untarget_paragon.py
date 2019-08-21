from paragon_utils import *
from shared_utils import *
from json_win_rates import * 

win_pcts, num_games, game_count, archetypes, overall_wr = get_win_pcts(min_game_threshold=0, min_game_count=0,limitTop=100)

archetypes = [
    "Control Warrior",
    "Highlander Mage",
    "Combo Priest",
    "Tempo Rogue",
    "Secret Hunter",
    "Quest Shaman",
    "Murloc Paladin",
    #"Control Mage",
    #"Quest Paladin",
    "Zoo Warlock",
    "Highlander Hunter",
    #"Quest Rogue",
    #"Quest Druid",
    #"Big Spell Mage",
    #"Aggro Warrior",
    #"Mech Hunter",
    #"Malygos Quest Druid",
]

lineups, archetype_map = generate_lineups(archetypes)
reverse_am = {}
for i in archetype_map:
    reverse_am[archetype_map[i]] = i
print(len(lineups))
print(archetype_map)
win_pcts_int = {}

for i in archetype_map:
    for j in archetype_map:
        if i != j:
            win_pcts_int[(i,j)] = win_pcts[(archetype_map[i], archetype_map[j])]
            
print(lineups[0])

def print_lineup(lineup, archetype_map):
    return ",".join([archetype_map[d] for d in lineup])

res = {}
count = 0
x = len(lineups)
print ( "total ", x, x * (x+1) / 2)
#for i in range(0, len(lineups) - 1):
#for i in range(0, len(lineups) - 1):
for i in range(0, 1):
    for j in range(i, len(lineups)):
        count += 1
        #print(count)
        #l1 = lineups[i]
        #l1 = (0, 1, 3, 4)
        l1 = tuple([reverse_am[i] for i in "Secret Hunter,Highlander Mage,Tempo Rogue,Control Warrior".split(',')])
        l2 = lineups[j]
        #print_lineup(l1, archetype_map)
        try:
            wr = protect_phase(l1, l2, win_pcts_int)[0]
            print(print_lineup(l2, archetype_map), wr)
            if l1 not in res:
                res[l1] = []
            if l2 not in res:
                res[l2] = []
            res[l1].append(wr)
            res[l2].append(1-wr)
        except:
            print("Skipping " + print_lineup(l1, archetype_map) + " vs " + print_lineup(l2, archetype_map))
        
#for i in res:
#    print(print_lineup(i, archetype_map), min(res[i]))

