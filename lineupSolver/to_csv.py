import sys
from json_win_rates import *


output_file = sys.argv[1]

#archetypes_allowed = [ 'Spiteful Druid', 'Taunt Druid', 'Quest Druid', 'Togwaggle Druid', 'Token Druid', 'Spell Hunter', 'Odd Hunter', 'Tempo Mage', 'Big Spell Mage', 'Even Paladin', 'Murloc Paladin', 'Odd Paladin', 'Control Paladin', 'Control Priest', 'Combo Priest', 'Quest Rogue', 'Odd Rogue', 'Miracle Rogue', 'Shudderwock Shaman', 'Control Warlock', 'Cube Warlock', 'Odd Warrior', 'Control Warrior', 'Quest Warrior', 'Odd Quest Warrior']

win_pcts, num_games, game_count, archetypes, overall_wr = get_win_pcts(min_game_threshold=0, min_game_count=0, limitTop=40)
archetypes = ["Control Priest", "Control Warlock", "Cube Warlock", "Even Paladin", "Miracle Rogue", "Murloc Paladin", "Odd Rogue", "Odd Warrior", "Quest Druid", "Quest Rogue", "Quest Warrior", "Spell Hunter", "Spiteful Druid", "Taunt Druid", "Tempo Mage", "Even Shaman"]
output = open(output_file, 'w')
#archetypes = archetypes_allowed
archetypes = sorted(archetypes, key=lambda x:game_count.get(x, 0), reverse=True)
res = wr_to_csv(win_pcts, archetypes, 100)
for line in res:
    output.write(line)
output.close()
