import sys
sys.path.append('../')
from config import basedir
sys.path.append(basedir)
sys.path.append(basedir + '/lineupSolver')

from shared_utils import *
from json_win_rates import * 
from conquest_utils import * 

lineups_to_test = [
    "Spiteful Druid,Murloc Paladin,Control Priest,Control Warlock",
    "Spiteful Druid,Tempo Mage,Quest Rogue,Cube Warlock",
    "Taunt Druid,Control Priest,Quest Rogue,Cube Warlock",
    "Taunt Druid,Even Paladin,Control Priest,Control Warlock",
    "Spiteful Druid,Control Priest,Quest Rogue,Control Warlock",
    "Taunt Druid,Combo Priest,Quest Rogue,Control Warlock",
    "Taunt Druid,Control Priest,Control Warlock,Odd Warrior",
    "Spiteful Druid,Tempo Mage,Even Paladin,Cube Warlock",
    "Spiteful Druid,Even Paladin,Control Priest,Control Warlock",
    "Tempo Mage,Even Paladin,Quest Rogue,Cube Warlock",
    "Taunt Druid,Control Priest,Control Warlock,Odd Warrior",
    "Odd Hunter,Tempo Mage,Murloc Paladin,Odd Rogue",
    "Even Paladin,Control Priest,Control Warlock,Odd Warrior",
    "Spiteful Druid,Spell Hunter,Control Warlock,Quest Warrior",
    "Taunt Druid,Control Priest,Miracle Rogue,Cube Warlock",
    "Big Spell Mage,Even Paladin,Cube Warlock,Odd Warrior",
    "Spiteful Druid,Tempo Mage,Control Warlock,Odd Warrior",
    "Even Paladin,Control Priest,Control Warlock,Quest Warrior",
    "Taunt Druid,Tempo Mage,Control Priest,Control Warlock",
    "Spiteful Druid,Even Paladin,Cube Warlock,Odd Warrior",
    "Even Paladin,Control Priest,Cube Warlock,Odd Warrior",
    "Spiteful Druid,Big Spell Mage,Cube Warlock,Quest Warrior",
    "Spiteful Druid,Big Spell Mage,Even Paladin,Cube Warlock",
    "Tempo Mage,Murloc Paladin,Odd Rogue,Cube Warlock",
    "Taunt Druid,Big Spell Mage,Control Warlock,Odd Warrior",
    "Spiteful Druid,Tempo Mage,Even Paladin,Quest Rogue",
    "Control Priest,Shudderwock Shaman,Control Warlock,Odd Warrior",
    "Taunt Druid,Big Spell Mage,Quest Rogue,Control Warlock",
    "Tempo Mage,Even Paladin,Control Priest,Cube Warlock",
    "Tempo Mage,Even Paladin,Odd Rogue,Cube Warlock",
    "Spiteful Druid,Control Priest,Quest Rogue,Cube Warlock",
    "Taunt Druid,Control Priest,Quest Rogue,Control Warlock",
    "Taunt Druid,Even Paladin,Control Warlock,Odd Warrior",
    "Control Priest,Miracle Rogue,Cube Warlock,Odd Quest Warrior",
    "Taunt Druid,Control Priest,Control Warlock,Quest Warrior",
    "Quest Druid,Control Priest,Quest Rogue,Cube Warlock",
    "Taunt Druid,Even Paladin,Control Priest,Cube Warlock",
    "Token Druid,Spell Hunter,Odd Paladin,Odd Warrior",
    "Quest Druid,Control Priest,Quest Rogue,Control Warlock",
    "Big Spell Mage,Control Priest,Control Warlock,Odd Quest Warrior",
    "Taunt Druid,Spell Hunter,Big Spell Mage,Cube Warlock",
    "Spiteful Druid,Control Priest,Cube Warlock,Odd Quest Warrior",
    "Tempo Mage,Even Paladin,Combo Priest,Cube Warlock",
]
lineups_to_test = [l.split(',') for l in lineups_to_test]
weights = [5,5,4,4,3,3,3,3,3,2,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
win_pcts, num_games, game_count, archetypes, overall_wr = get_win_pcts(min_game_threshold=0, min_game_count=0,limitTop=140)
