from __future__ import print_function
import sys
sys.path.append('../')
from config import basedir
sys.path.append(basedir)
sys.path.append(basedir + '/lineupSolver')
from shared_utils import *
import itertools
from pprint import pprint
from battlefy_decks_results import *

urls = ['https://battlefy.com/hearthstone-esports/2018-americas-fall-playoffs/5b5902c01773a803a47759c0/stage/5b9d14d4d59a6903a15c46f4/bracket/']

decks = {
    "PNC"                : "Taunt Druid,Deathrattle Hunter,Quest Rogue,Even Warlock",
    "Nalguidan"          : "Taunt Druid,Deathrattle Hunter,Quest Rogue,Even Warlock",
    "Tarei"              : "Malygos Tog Druid,Quest Rogue,Shudderwock Shaman,Cube Warlock",
    "SnipedAgain"        : "Secret Hunter,Tempo Mage,Odd Rogue,Zoo Warlock",
    "dog"                : "Taunt Druid,Deathrattle Hunter,Quest Rogue,Even Warlock",
    "Ant"                : "Taunt Token Druid,Quest Rogue,Shudderwock Shaman,Even Warlock",
    "Firebat"            : "Taunt Token Druid,Secret Hunter,Odd Rogue,Odd Warrior",
    "Purple"             : "Taunt Token Druid,Secret Hunter,Odd Rogue,Odd Warrior",
    "HotMEOWTH"          : "Taunt Druid,Deathrattle Hunter,Quest Rogue,Shudderwock Shaman",
    "Tincho"             : "Taunt Token Druid,Secret Hunter,Odd Rogue,Zoo Warlock",
    "Aviera"             : "Malygos Tog Druid,Deathrattle Hunter,Shudderwock Shaman,Odd Warrior",
    "Conrad"             : "Mill Druid,Deathrattle Hunter,Quest Rogue,Even Warlock",
    "muzzy"              : "Taunt Token Druid,Secret Hunter,Odd Paladin,Odd Rogue",
    "Activelee"          : "Taunt Token Druid,Secret Hunter,Odd Rogue,Zoo Warlock",
    "Akatsu"             : "Token Druid,Quest Rogue,Shudderwock Shaman,Even Warlock",
    "UchihaSaske"        : "Mill Druid,Shudderwock Shaman,Even Warlock,Odd Warrior",
    "Rase"               : "Taunt Druid,Deathrattle Hunter,Quest Rogue,Cube Warlock",
    "Qwerty97"           : "Big Druid,Secret Hunter,Even Warlock,Quest Warrior",
    "fibonacci"          : "Mill Druid,Control Priest,Even Warlock,Control Warrior",
    "Nostam"             : "Taunt Token Druid,Secret Hunter,Odd Paladin,Odd Rogue",
    "HockeyBoyz3"        : "Malygos Druid,Mecha'thun Priest,Mecha'thun Warlock,Mecha'thun Warrior",
    "Lyme"               : "Mill Druid,Secret Hunter,Control Priest,Odd Warrior",
    "Pelletire"          : "Taunt Druid,Deathrattle Hunter,Quest Rogue,Cube Warlock",
    "lii"                : "Malygos Druid,Combo Priest,Odd Rogue,Even Warlock",
    "seiger"             : "Taunt Druid,Deathrattle Hunter,Quest Rogue,Even Warlock",
    "Rosty"              : "Mill Druid,Spell Hunter,Control Priest,Odd Warrior",
    "Gladen"             : "Taunt Token Druid,Deathrattle Hunter,Shudderwock Shaman,Even Warlock",
    "Ike"                : "Taunt Token Druid,Odd Rogue,Midrange Shaman,Even Warlock",
    "zaguios"            : "Token Druid,Odd Paladin,Odd Rogue,Zoo Warlock",
    "ironFIRE"           : "Taunt Druid,Deathrattle Hunter,Shudderwock Pyro Shaman,Cube Warlock",
    "fr0zen"             : "Taunt Druid,Deathrattle Hunter,Even Warlock,Odd Warrior",
    "bloodyface"         : "Malygos Druid,Deathrattle Hunter,Quest Rogue,Even Warlock",
    "yoitsflo"           : "Taunt Token Druid,Secret Hunter,Odd Paladin,Odd Rogue",
    "cowboys367"         : "Taunt Token Druid,Secret Hunter,Odd Rogue,Even Warlock",
    "Apxvoid"            : "Taunt Druid,Deathrattle Hunter,Even Warlock,Odd Warrior",
    "Kevor24"            : "Secret Hunter,Odd Rogue,Even Shaman,Even Warlock",
    "wiz"                : "Malygos Druid,Control Priest,Quest Rogue,Even Warlock",
    "lnguagehackr"       : "Taunt Druid,Quest Rogue,Shudderwock Pyro Shaman,Cube Warlock",
    "noblord"            : "Malygos Druid,Quest Rogue,Shudderwock Shaman,Even Warlock",
    "killinallday"       : "Taunt Token Druid,Quest Rogue,Shudderwock Shaman,Even Warlock",
    "Cydonia"            : "Taunt Token Druid,Shudderwock Shaman,Even Warlock,Odd Warrior",
    "Monsanto"           : "Malygos Druid,Tempo Mage,Quest Rogue,Even Warlock",
    "zalae"              : "Taunt Token Druid,Quest Rogue,Even Warlock,Odd Quest Warrior",
    "Pal"                : "Token Druid,Odd Paladin,Odd Rogue,Odd Warrior",
    "villain"            : "Malygos Druid,Control Priest,Quest Rogue,Even Warlock",
    "justsaiyan"         : "Taunt Token Druid,Secret Hunter,Odd Rogue,Zoo Warlock",
    "strifecro"          : "Taunt Token Druid,Deathrattle Hunter,Quest Rogue,Zoo Warlock",
    "Fled"               : "Taunt Druid,Deathrattle Hunter,Quest Rogue,Even Warlock",
    "BlasèBlasè"         : "Token Druid,Secret Hunter,Odd Rogue,Zoo Warlock",
    "Cheese"             : "OTK DK Paladin,Shudderwock Pyro Shaman,Mecha'thun Warlock,Control Warrior",
    "korextron"          : "Malygos Tog Druid,Control Priest,Odd Rogue,Even Warlock",
    "zlsjs"              : "Malygos Druid,Control Priest,Quest Rogue,Even Warlock",
    "Gallon"             : "Taunt Token Druid,Secret Hunter,Odd Rogue,Odd Warrior",
    "amnesiac"           : "Taunt Token Druid,Secret Hunter,Odd Paladin,Odd Rogue",
    "Ryder"              : "Big Druid,Secret Hunter,Even Warlock,Quest Warrior",
    "control"            : "Taunt Token Druid,Secret Hunter,Quest Rogue,Zoo Warlock",
    "caravaggio8"        : "Malygos Druid,Control Priest,Quest Rogue,Even Warlock",
    "Jonahrah"           : "Taunt Token Druid,Secret Hunter,Quest Rogue,Zoo Warlock",
    "SwaggyG"            : "Taunt Token Druid,Quest Rogue,Shudderwock Shaman,Even Warlock",
    "Joaquin"            : "Tempo Mage,Odd Paladin,Odd Rogue,Zoo Warlock",
    "Cesky"              : "Taunt Token Druid,Quest Rogue,Shudderwock Shaman,Cube Warlock",
    "Ownerism"           : "Malygos Druid,Odd Rogue,Even Shaman,Even Warlock",
    "seohyun628"         : "Taunt Druid,Deathrattle Hunter,Quest Rogue,Shudderwock Shaman",
    "Alan870806"         : "Malygos Druid,Quest Rogue,Shudderwock Shaman,Even Warlock",
    "Kuonet"             : "Taunt Druid,Deathrattle Hunter,Shudderwock Shaman,Even Warlock",
    "Starfruit"          : "Taunt Token Druid,Secret Hunter,Odd Rogue,Even Warlock",
    "Zamos"              : "Malygos Druid,Shudderwock Shaman,Cube Warlock,Control Warrior",
    "klei"               : "Control Priest,Quest Rogue,Cube Warlock,Odd Warrior",
    "HSKeDaiBiao"        : "Taunt Token Druid,Odd Paladin,Odd Rogue,Zoo Warlock",
    "ETC"                : "Mill Druid,Quest Rogue,Shudderwock Shaman,Even Warlock",
    "bobbyex"            : "Taunt Token Druid,Deathrattle Hunter,Quest Rogue,Even Warlock",
    "NoHandsGamer"       : "Token Druid,Spell Hunter,Control Priest,Odd Warrior",
    "jakaso27"           : "Big Druid,Secret Hunter,Even Warlock,Quest Warrior",
    "PrinceFancy"        : "Taunt Druid,Shudderwock Pyro Shaman,Control Warlock,Odd Warrior",
    "Justine"            : "Taunt Token Druid,Control Priest,Even Warlock,Odd Warrior",
    "TheMaverick"        : "Mill Druid,Deathrattle Hunter,Quest Rogue,Shudderwock Pyro Shaman",
    "InquisitorM"        : "Token Druid,Secret Hunter,Odd Paladin,Control Priest",
}

archetype_map = {}
for p in decks:
    decks[p] = decks[p].split(',')
    for i in decks[p]:
        archetype_map[(p, i.split(' ')[-1].lower())] = i

player_matches = {}
archetypes = {}
all_matches = []
unlabeled = {}
for url in urls:
    #tmp_decks, tmp_matches, tmp_player_matches = process_battlefy_url(url)
    tmp_decks, tmp_matches, tmp_player_matches = process_battlefy_url(url, only_finished=True)
    # this is not quite right because could be lists to append to
    for i,j in tmp_player_matches.items():
        player_matches[i] = player_matches.get(i, []) + j
    #player_matches.update(tmp_player_matches)
    all_matches += tmp_matches

wins = {}
games = {}
for match in all_matches:
    p1, p2 = match[2:4]
    #print(match)
    for game in match[-1]:
        c1, c2, res = game
        try:
            d1 = archetype_map[(p1, c1)]
        except:
            print('mismatch %s %s' % (p1, c1))
        try:
            d2 = archetype_map[(p2, c2)]
        except:
            print('mismatch %s %s' % (p2, c2))
        games[(d1, d2)] = games.get((d1, d2), 0) + 1
        games[(d2, d1)] = games.get((d2, d1), 0) + 1
        if res:
            wins[(d1, d2)] = wins.get((d1, d2), 0) + 1
        else:
            wins[(d2, d1)] = wins.get((d2, d1), 0) + 1

decks = {
    "PNC"                : "Taunt Druid,Deathrattle Hunter,Quest Rogue,Even Warlock",
    "Nalguidan"          : "Taunt Druid,Deathrattle Hunter,Quest Rogue,Even Warlock",
    "Tarei"              : "Malygos Tog Druid,Quest Rogue,Shudderwock Shaman,Cube Warlock",
    "SnipedAgain"        : "Secret Hunter,Tempo Mage,Odd Rogue,Zoo Warlock",
    "dog"                : "Taunt Druid,Deathrattle Hunter,Quest Rogue,Even Warlock",
    "Ant"                : "Taunt Token Druid,Quest Rogue,Shudderwock Shaman,Even Warlock",
    "Firebat"            : "Taunt Token Druid,Secret Hunter,Odd Rogue,Odd Warrior",
    "Purple"             : "Taunt Token Druid,Secret Hunter,Odd Rogue,Odd Warrior",
    "HotMEOWTH"          : "Taunt Druid,Deathrattle Hunter,Quest Rogue,Shudderwock Shaman",
    "Tincho"             : "Taunt Token Druid,Secret Hunter,Odd Rogue,Zoo Warlock",
    "Aviera"             : "Malygos Tog Druid,Deathrattle Hunter,Shudderwock Shaman,Odd Warrior",
    "Conrad"             : "Mill Druid,Deathrattle Hunter,Quest Rogue,Even Warlock",
    "muzzy"              : "Taunt Token Druid,Secret Hunter,Odd Paladin,Odd Rogue",
    "Activelee"          : "Taunt Token Druid,Secret Hunter,Odd Rogue,Zoo Warlock",
    "Akatsu"             : "Token Druid,Quest Rogue,Shudderwock Shaman,Even Warlock",
    "UchihaSaske"        : "Mill Druid,Shudderwock Shaman,Even Warlock,Odd Warrior",
    "Rase"               : "Taunt Druid,Deathrattle Hunter,Quest Rogue,Cube Warlock",
    "Qwerty97"           : "Big Druid,Secret Hunter,Even Warlock,Quest Warrior",
    "fibonacci"          : "Mill Druid,Control Priest,Even Warlock,Control Warrior",
    "Nostam"             : "Taunt Token Druid,Secret Hunter,Odd Paladin,Odd Rogue",
    "HockeyBoyz3"        : "Malygos Druid,Mecha'thun Priest,Mecha'thun Warlock,Mecha'thun Warrior",
    "Lyme"               : "Mill Druid,Secret Hunter,Control Priest,Odd Warrior",
    "Pelletire"          : "Taunt Druid,Deathrattle Hunter,Quest Rogue,Cube Warlock",
    "lii"                : "Malygos Druid,Combo Priest,Odd Rogue,Even Warlock",
    "seiger"             : "Taunt Druid,Deathrattle Hunter,Quest Rogue,Even Warlock",
    "Rosty"              : "Mill Druid,Spell Hunter,Control Priest,Odd Warrior",
    "Gladen"             : "Taunt Token Druid,Deathrattle Hunter,Shudderwock Shaman,Even Warlock",
    "Ike"                : "Taunt Token Druid,Odd Rogue,Midrange Shaman,Even Warlock",
    "zaguios"            : "Token Druid,Odd Paladin,Odd Rogue,Zoo Warlock",
    "ironFIRE"           : "Taunt Druid,Deathrattle Hunter,Shudderwock Pyro Shaman,Cube Warlock",
    "fr0zen"             : "Taunt Druid,Deathrattle Hunter,Even Warlock,Odd Warrior",
    "bloodyface"         : "Malygos Druid,Deathrattle Hunter,Quest Rogue,Even Warlock",
    "yoitsflo"           : "Taunt Token Druid,Secret Hunter,Odd Paladin,Odd Rogue",
    "cowboys367"         : "Taunt Token Druid,Secret Hunter,Odd Rogue,Even Warlock",
    "Apxvoid"            : "Taunt Druid,Deathrattle Hunter,Even Warlock,Odd Warrior",
    "Kevor24"            : "Secret Hunter,Odd Rogue,Even Shaman,Even Warlock",
    "wiz"                : "Malygos Druid,Control Priest,Quest Rogue,Even Warlock",
    "lnguagehackr"       : "Taunt Druid,Quest Rogue,Shudderwock Pyro Shaman,Cube Warlock",
    "noblord"            : "Malygos Druid,Quest Rogue,Shudderwock Shaman,Even Warlock",
    "killinallday"       : "Taunt Token Druid,Quest Rogue,Shudderwock Shaman,Even Warlock",
    "Cydonia"            : "Taunt Token Druid,Shudderwock Shaman,Even Warlock,Odd Warrior",
    "Monsanto"           : "Malygos Druid,Tempo Mage,Quest Rogue,Even Warlock",
    "zalae"              : "Taunt Token Druid,Quest Rogue,Even Warlock,Odd Quest Warrior",
    "Pal"                : "Token Druid,Odd Paladin,Odd Rogue,Odd Warrior",
    "villain"            : "Malygos Druid,Control Priest,Quest Rogue,Even Warlock",
    "justsaiyan"         : "Taunt Token Druid,Secret Hunter,Odd Rogue,Zoo Warlock",
    "strifecro"          : "Taunt Token Druid,Deathrattle Hunter,Quest Rogue,Zoo Warlock",
    "Fled"               : "Taunt Druid,Deathrattle Hunter,Quest Rogue,Even Warlock",
    "BlasèBlasè"         : "Token Druid,Secret Hunter,Odd Rogue,Zoo Warlock",
    "Cheese"             : "OTK DK Paladin,Shudderwock Pyro Shaman,Mecha'thun Warlock,Control Warrior",
    "korextron"          : "Malygos Tog Druid,Control Priest,Odd Rogue,Even Warlock",
    "zlsjs"              : "Malygos Druid,Control Priest,Quest Rogue,Even Warlock",
    "Gallon"             : "Taunt Token Druid,Secret Hunter,Odd Rogue,Odd Warrior",
    "amnesiac"           : "Taunt Token Druid,Secret Hunter,Odd Paladin,Odd Rogue",
    "Ryder"              : "Big Druid,Secret Hunter,Even Warlock,Quest Warrior",
    "control"            : "Taunt Token Druid,Secret Hunter,Quest Rogue,Zoo Warlock",
    "caravaggio8"        : "Malygos Druid,Control Priest,Quest Rogue,Even Warlock",
    "Jonahrah"           : "Taunt Token Druid,Secret Hunter,Quest Rogue,Zoo Warlock",
    "SwaggyG"            : "Taunt Token Druid,Quest Rogue,Shudderwock Shaman,Even Warlock",
    "Joaquin"            : "Tempo Mage,Odd Paladin,Odd Rogue,Zoo Warlock",
    "Cesky"              : "Taunt Token Druid,Quest Rogue,Shudderwock Shaman,Cube Warlock",
    "Ownerism"           : "Malygos Druid,Odd Rogue,Even Shaman,Even Warlock",
    "seohyun628"         : "Taunt Druid,Deathrattle Hunter,Quest Rogue,Shudderwock Shaman",
    "Alan870806"         : "Malygos Druid,Quest Rogue,Shudderwock Shaman,Even Warlock",
    "Kuonet"             : "Taunt Druid,Deathrattle Hunter,Shudderwock Shaman,Even Warlock",
    "Starfruit"          : "Taunt Token Druid,Secret Hunter,Odd Rogue,Even Warlock",
    "Zamos"              : "Malygos Druid,Shudderwock Shaman,Cube Warlock,Control Warrior",
    "klei"               : "Control Priest,Quest Rogue,Cube Warlock,Odd Warrior",
    "HSKeDaiBiao"        : "Taunt Token Druid,Odd Paladin,Odd Rogue,Zoo Warlock",
    "ETC"                : "Mill Druid,Quest Rogue,Shudderwock Shaman,Even Warlock",
    "bobbyex"            : "Taunt Token Druid,Deathrattle Hunter,Quest Rogue,Even Warlock",
    "NoHandsGamer"       : "Token Druid,Spell Hunter,Control Priest,Odd Warrior",
    "jakaso27"           : "Big Druid,Secret Hunter,Even Warlock,Quest Warrior",
    "PrinceFancy"        : "Taunt Druid,Shudderwock Pyro Shaman,Control Warlock,Odd Warrior",
    "Justine"            : "Taunt Token Druid,Control Priest,Even Warlock,Odd Warrior",
    "TheMaverick"        : "Mill Druid,Deathrattle Hunter,Quest Rogue,Shudderwock Pyro Shaman",
    "InquisitorM"        : "Token Druid,Secret Hunter,Odd Paladin,Control Priest",
}

filename = 'custom_na.csv'
win_pcts, archetypes = wr_from_csv(filename, scaling=100)

for i,j in sorted(games.items(), key=lambda x:x[1], reverse=True):
    w = wins.get(i, 0)
    pct = round(w / j, 3)
    a,b = i
    l = j - w
    #print("%-20s %-20s %s-%s %5s" % (a,b, w, l, pct))
    print("%s,%s,%s,%s,%s" % (a,b, w, l, pct))
