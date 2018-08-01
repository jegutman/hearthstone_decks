import sys
from json_win_rates import *


output_file = sys.argv[1]

#archetypes_allowed = [ 'Spiteful Druid', 'Taunt Druid', 'Quest Druid', 'Togwaggle Druid', 'Token Druid', 'Spell Hunter', 'Odd Hunter', 'Tempo Mage', 'Big Spell Mage', 'Even Paladin', 'Murloc Paladin', 'Odd Paladin', 'Control Paladin', 'Control Priest', 'Combo Priest', 'Quest Rogue', 'Odd Rogue', 'Miracle Rogue', 'Shudderwock Shaman', 'Control Warlock', 'Cube Warlock', 'Odd Warrior', 'Control Warrior', 'Quest Warrior', 'Odd Quest Warrior']

win_pcts, num_games, game_count, archetypes, overall_wr = get_win_pcts(min_game_threshold=0, min_game_count=0, limitTop=40)
#archetypes = ["Control Priest", "Control Warlock", "Cube Warlock", "Even Paladin", "Miracle Rogue", "Murloc Paladin", "Odd Rogue", "Odd Warrior", "Quest Druid", "Quest Rogue", "Quest Warrior", "Spell Hunter", "Spiteful Druid", "Taunt Druid", "Tempo Mage", "Even Shaman"]
archetypes = ["Control Priest", "Zoo Warlock", "Even Warlock", "Odd Paladin", "Miracle Rogue", "Quest Warrior", "Malygos Druid", "Deathrattle Hunter", "Tempo Mage", "Shudderwock Shaman"]
archetypes.sort(key=lambda x:x.split(' ')[-1])
#l1 = ['Even Warlock', 'Odd Paladin', 'Control Priest', 'Tempo Mage', 'Deathrattle Hunter', 'Miracle Rogue', 'Shudderwock Shaman', 'Quest Warrior', 'Malygos Druid']
#l2 = ['Even Warlock', 'Odd Paladin', 'Control Priest', 'Big Spell Mage', 'Recruit Hunter', 'Miracle Rogue', 'Shudderwock Shaman', 'Odd Warrior', 'Token Druid']

#l1 = "Malygos Druid,Even Warlock,Shudderwock Shaman,Odd Rogue,Deathrattle Hunter,Odd Paladin,Quest Warrior,Control Priest,Big Spell Mage".split(',')
#l2 = "Recruit Hunter,Quest Warrior,Odd Paladin,Taunt Druid,Control Priest,Even Warlock,Shudderwock Shaman,Big Spell Mage,Miracle Rogue".split(',')
#l2 = "Shudderwock Shaman,Odd Paladin,Mill Druid,Murloc Mage,Zoo Warlock,Combo Priest,Odd Rogue,Deathrattle Hunter,Quest Warrior".split(',')
l1 = "Quest Warrior,Quest Priest,Shudderwock Shaman,Zoo Warlock,Odd Paladin,Odd Rogue,Murloc Mage,Token Druid,Deathrattle Hunter".split(',')
l2 = "Quest Warrior,Control Priest,Even Shaman,Zoo Warlock,Odd Paladin,Miracle Rogue,Tempo Mage,Malygos Druid,Deathrattle Hunter".split(',')

output = open(output_file, 'w')
#archetypes = archetypes_allowed
#archetypes = sorted(archetypes, key=lambda x:game_count.get(x, 0), reverse=True)
archetypes.sort(key=lambda x:x.split(' ')[-1])
#res = wr_to_csv(win_pcts, archetypes, 100)
res = wr_to_csv(win_pcts, l1, l2, 100)
print(res)
for line in res:
    output.write(line)
output.close()
