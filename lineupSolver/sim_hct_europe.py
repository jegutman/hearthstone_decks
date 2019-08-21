import sys
sys.path.append('../')
from config import basedir
sys.path.append(basedir)
sys.path.append(basedir + '/lineupSolver')


from shared_utils import *
from json_win_rates import * 
from conquest_utils import * 
from sim_matchup import *

from random import shuffle

decks = {
    "PNC"                : "Taunt Druid,Deathrattle Hunter,Quest Rogue,Even Warlock",
    "Nalguidan"          : "Taunt Druid,Deathrattle Hunter,Quest Rogue,Even Warlock",
    "Tarei"              : "Malygos Druid,Quest Rogue,Shudderwock Shaman,Cube Warlock",
    "SnipedAgain"        : "Midrange Hunter,Tempo Mage,Odd Rogue,Zoo Warlock",
    "dog"                : "Taunt Druid,Deathrattle Hunter,Quest Rogue,Even Warlock",
    "Ant"                : "Token Druid,Quest Rogue,Shudderwock Shaman,Even Warlock",
    "Firebat"            : "Token Druid,Midrange Hunter,Odd Rogue,Odd Warrior",
    "Purple"             : "Token Druid,Midrange Hunter,Odd Rogue,Odd Warrior",
    "HotMEOWTH"          : "Taunt Druid,Deathrattle Hunter,Quest Rogue,Shudderwock Shaman",
    "Tincho"             : "Token Druid,Midrange Hunter,Odd Rogue,Zoo Warlock",
    "Aviera"             : "Malygos Druid,Deathrattle Hunter,Shudderwock Shaman,Odd Warrior",
    "Conrad"             : "Mill Druid,Deathrattle Hunter,Quest Rogue,Even Warlock",
    "muzzy"              : "Token Druid,Midrange Hunter,Odd Paladin,Odd Rogue",
    "Activelee"          : "Token Druid,Midrange Hunter,Odd Rogue,Zoo Warlock",
    "Akatsu"             : "Token Druid,Quest Rogue,Shudderwock Shaman,Even Warlock",
    "UchihaSaske"        : "Mill Druid,Shudderwock Shaman,Even Warlock,Odd Warrior",
    "Rase"               : "Taunt Druid,Deathrattle Hunter,Quest Rogue,Cube Warlock",
    "Qwerty97"           : "Big Druid,Midrange Hunter,Even Warlock,Quest Warrior",
    "fibonacci"          : "Mill Druid,Control Priest,Even Warlock,Control Warrior",
    "Nostam"             : "Token Druid,Midrange Hunter,Odd Paladin,Odd Rogue",
    "HockeyBoyz3"        : "Malygos Druid,Mecha'thun Priest,Mecha'thun Warlock,Mecha'thun Warrior",
    "Lyme"               : "Mill Druid,Midrange Hunter,Control Priest,Odd Warrior",
    "Pelletire"          : "Taunt Druid,Deathrattle Hunter,Quest Rogue,Cube Warlock",
    "lii"                : "Malygos Druid,Combo Priest,Odd Rogue,Even Warlock",
    "seiger"             : "Taunt Druid,Deathrattle Hunter,Quest Rogue,Even Warlock",
    "Rosty"              : "Mill Druid,Spell Hunter,Control Priest,Odd Warrior",
    "Gladen"             : "Token Druid,Deathrattle Hunter,Shudderwock Shaman,Even Warlock",
    "Ike"                : "Token Druid,Odd Rogue,Token Shaman,Even Warlock",
    "zaguios"            : "Token Druid,Odd Paladin,Odd Rogue,Zoo Warlock",
    "ironFIRE"           : "Taunt Druid,Deathrattle Hunter,Shudderwock Shaman,Cube Warlock",
    "fr0zen"             : "Taunt Druid,Deathrattle Hunter,Even Warlock,Odd Warrior",
    "bloodyface"         : "Malygos Druid,Deathrattle Hunter,Quest Rogue,Even Warlock",
    "yoitsflo"           : "Token Druid,Midrange Hunter,Odd Paladin,Odd Rogue",
    "cowboys367"         : "Token Druid,Midrange Hunter,Odd Rogue,Even Warlock",
    "Apxvoid"            : "Taunt Druid,Deathrattle Hunter,Even Warlock,Odd Warrior",
    "Kevor24"            : "Midrange Hunter,Odd Rogue,Even Shaman,Even Warlock",
    "wiz"                : "Malygos Druid,Control Priest,Quest Rogue,Even Warlock",
    "lnguagehackr"       : "Taunt Druid,Quest Rogue,Shudderwock Shaman,Cube Warlock",
    "noblord"            : "Malygos Druid,Quest Rogue,Shudderwock Shaman,Even Warlock",
    "killinallday"       : "Token Druid,Quest Rogue,Shudderwock Shaman,Even Warlock",
    "Cydonia"            : "Token Druid,Shudderwock Shaman,Even Warlock,Odd Warrior",
    "Monsanto"           : "Malygos Druid,Tempo Mage,Quest Rogue,Even Warlock",
    "zalae"              : "Token Druid,Quest Rogue,Even Warlock,Odd Quest Warrior",
    "Pal"                : "Token Druid,Odd Paladin,Odd Rogue,Odd Warrior",
    "villain"            : "Malygos Druid,Control Priest,Quest Rogue,Even Warlock",
    "justsaiyan"         : "Token Druid,Midrange Hunter,Odd Rogue,Zoo Warlock",
    "strifecro"          : "Token Druid,Deathrattle Hunter,Quest Rogue,Zoo Warlock",
    "Fled"               : "Taunt Druid,Deathrattle Hunter,Quest Rogue,Even Warlock",
    "BlasèBlasè"         : "Token Druid,Midrange Hunter,Odd Rogue,Zoo Warlock",
    "Cheese"             : "OTK DK Paladin,Shudderwock Shaman,Mecha'thun Warlock,Control Warrior",
    "korextron"          : "Mill Druid,Control Priest,Odd Rogue,Even Warlock",
    "zlsjs"              : "Malygos Druid,Control Priest,Quest Rogue,Even Warlock",
    "Gallon"             : "Token Druid,Midrange Hunter,Odd Rogue,Odd Warrior",
    "amnesiac"           : "Token Druid,Midrange Hunter,Odd Paladin,Odd Rogue",
    "Ryder"              : "Big Druid,Midrange Hunter,Even Warlock,Quest Warrior",
    "control"            : "Token Druid,Midrange Hunter,Quest Rogue,Zoo Warlock",
    "caravaggio8"        : "Malygos Druid,Control Priest,Quest Rogue,Even Warlock",
    "Jonahrah"           : "Token Druid,Midrange Hunter,Quest Rogue,Zoo Warlock",
    "SwaggyG"            : "Token Druid,Quest Rogue,Shudderwock Shaman,Even Warlock",
    "Joaquin"            : "Tempo Mage,Odd Paladin,Odd Rogue,Zoo Warlock",
    "Cesky"              : "Token Druid,Quest Rogue,Shudderwock Shaman,Cube Warlock",
    "Ownerism"           : "Malygos Druid,Odd Rogue,Even Shaman,Even Warlock",
    "seohyun628"         : "Taunt Druid,Deathrattle Hunter,Quest Rogue,Shudderwock Shaman",
    "Alan870806"         : "Malygos Druid,Quest Rogue,Shudderwock Shaman,Even Warlock",
    "Kuonet"             : "Taunt Druid,Deathrattle Hunter,Shudderwock Shaman,Even Warlock",
    "Starfruit"          : "Token Druid,Midrange Hunter,Odd Rogue,Even Warlock",
    "Zamos"              : "Malygos Druid,Shudderwock Shaman,Cube Warlock,Control Warrior",
    "klei"               : "Control Priest,Quest Rogue,Cube Warlock,Odd Warrior",
    "HSKeDaiBiao"        : "Token Druid,Odd Paladin,Odd Rogue,Zoo Warlock",
    "ETC"                : "Mill Druid,Quest Rogue,Shudderwock Shaman,Even Warlock",
    "bobbyex"            : "Token Druid,Deathrattle Hunter,Quest Rogue,Even Warlock",
    "NoHandsGamer"       : "Token Druid,Spell Hunter,Control Priest,Odd Warrior",
    "jakaso27"           : "Big Druid,Midrange Hunter,Even Warlock,Quest Warrior",
    "PrinceFancy"        : "Taunt Druid,Shudderwock Shaman,Control Warlock,Odd Warrior",
    "Justine"            : "Token Druid,Control Priest,Even Warlock,Odd Warrior",
    "TheMaverick"        : "Mill Druid,Deathrattle Hunter,Quest Rogue,Shudderwock Shaman",
    "InquisitorM"        : "Token Druid,Midrange Hunter,Odd Paladin,Control Priest",
}

win_pcts, num_games, game_count, archetypes, overall_wr = get_win_pcts(min_game_threshold=0, min_game_count=0,limitTop=100)
overrides = [
            ]
win_pcts = override_wr(overrides,win_pcts)

tops = {}

#def simulate_tournament(decks, rounds, scores=None, win_pcts={}):
#    if scores == None:
#        for d in decks:
#            scores[d.name] = 0
#    for i in range(0, rounds):
#        simulate_round(decks, scores, win_pcts)
#    return scores

d1 = decks[sys.argv[1]]
d2 = decks[sys.argv[2]]

print(calculate_win_rate(d1, d2, win_pcts))
print(sim(d1, d2))
print(cq_bans(d1, d2))
