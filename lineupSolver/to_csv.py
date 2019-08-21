import sys
from json_win_rates import *


output_file = sys.argv[1]

#archetypes_allowed = [ 'Spiteful Druid', 'Taunt Druid', 'Quest Druid', 'Togwaggle Druid', 'Token Druid', 'Spell Hunter', 'Odd Hunter', 'Tempo Mage', 'Big Spell Mage', 'Even Paladin', 'Murloc Paladin', 'Odd Paladin', 'Control Paladin', 'Control Priest', 'Combo Priest', 'Quest Rogue', 'Odd Rogue', 'Miracle Rogue', 'Shudderwock Shaman', 'Control Warlock', 'Cube Warlock', 'Odd Warrior', 'Control Warrior', 'Quest Warrior', 'Odd Quest Warrior']

win_pcts, num_games, game_count, archetypes, overall_wr = get_win_pcts(min_game_threshold=0, min_game_count=0, limitTop=30)

#filename = 'wr_na.csv'
#win_pcts2, archetypes = wr_from_csv(filename, scaling=100)
#win_pcts.update(win_pcts2)

#archetypes = ['Even Warlock', 'Quest Rogue', 'Token Druid', 'Odd Rogue', 'Shudderwock Shaman', 'Midrange Hunter', 'Deathrattle Hunter', 'Taunt Druid', 'Odd Warrior', 'Malygos Druid', 'Control Priest', 'Zoo Warlock', 'Odd Paladin', 'Cube Warlock', 'Mill Druid', 'Tempo Mage', 'Quest Warrior', 'Big Druid', 'Control Warrior', "Mecha'thun Warlock", 'Spell Hunter', 'Even Shaman', "Mecha'thun Warrior", "Mecha'thun Priest", 'Combo Priest', 'Token Shaman', 'Odd Quest Warrior', 'OTK DK Paladin', 'Control Warlock']

#archetypes = ["Control Priest", "Zoo Warlock", "Even Warlock", "Odd Paladin", "Miracle Rogue", "Quest Warrior", "Malygos Druid", "Deathrattle Hunter", "Tempo Mage", "Shudderwock Shaman"]
#archetypes.sort(key=lambda x:x.split(' ')[-1])
#l1 = ['Even Warlock', 'Odd Paladin', 'Control Priest', 'Tempo Mage', 'Deathrattle Hunter', 'Miracle Rogue', 'Shudderwock Shaman', 'Quest Warrior', 'Malygos Druid']
#l2 = ['Even Warlock', 'Odd Paladin', 'Control Priest', 'Big Spell Mage', 'Recruit Hunter', 'Miracle Rogue', 'Shudderwock Shaman', 'Odd Warrior', 'Token Druid']

archetypes = [
    'Tempo Rogue',
    'Zoo Warlock',
    'Control Warrior',
    'Midrange Hunter',
    'Khadgar Dragon Mage',
    'Bomb Warrior',
    'Control Shaman',
    'Miracle Rogue',
    'Token Druid',
    'Nomi Priest',
    'Heal Druid',
    'Token Shaman',
    'Mech Hunter',
]

#l1 = ['Token Druid', 'Taunt Druid', 'Big Druid', 'Malygos Druid', 'Spiteful Druid', 'Mill Druid', 'Deathrattle Hunter', 'Spell Hunter', 'Midrange Hunter', 'Tempo Mage', 'Odd Paladin', 'Mech Paladin', 'Odd Rogue', 'Kingsbane Rogue', 'Quest Rogue', 'Shudderwock Shaman', 'Midrange Shaman', 'Zoo Warlock', 'Control Warlock', 'Even Warlock', 'Odd Warrior']
l1 = archetypes
l2 = l1
#l1 = 'Odd Warrior,Control Priest,Shudderwock Shaman,Zoo Warlock,Odd Paladin,Quest Rogue,Tempo Mage,Token Druid,Deathrattle Hunter'.split(',')
#l2 = 'Odd Warrior,Control Priest,Shudderwock Shaman,Zoo Warlock,Odd Paladin,Odd Rogue,Tempo Mage,Token Druid,Secret Hunter'.split(',')


output = open(output_file, 'w')
#archetypes = archetypes_allowed
#archetypes = sorted(archetypes, key=lambda x:game_count.get(x, 0), reverse=True)
#archetypes.sort(key=lambda x:x.split(' ')[-1])
#res = wr_to_csv(win_pcts, archetypes, 100)
#res = wr_to_csv_diag(win_pcts, l1, other_archetypes=l2, scaling=100, rounding=2)
res = wr_to_csv(win_pcts, l1, other_archetypes=l2, scaling=100, rounding=2)
print(res)
for line in res:
    output.write(line)
output.close()
