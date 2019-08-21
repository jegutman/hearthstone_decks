from json_win_rates import * 
from lhs_utils import * 
from shared_utils import *

if __name__ == '__main__':
    level1, level2, level3, level4, level5 = None, None, None, None, None
    level1 = "Cube Warlock,Even Paladin,Control Priest,Odd Rogue".split(',')
    #level2 = "Zoo Warlock,Murloc Paladin,Spiteful Priest,Secret Mage".split(',')
    #level3 = "Cube Warlock,Combo Priest,Silver Hand Paladin,Quest Rogue".split(',')

    lineups_to_test = [l for l in [level1, level2, level3, level4, level5] if l is not None]
    tmp_weights = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    lineups_to_test = [
        "Malygos Druid,Deathrattle Hunter,Even Paladin,Shudderwock Shaman",
        "Spell Hunter,Even Paladin,Even Shaman,Even Warlock",
        "Taunt Druid,Deathrattle Hunter,Even Paladin,Shudderwock Shaman",
        "Odd Paladin,Odd Rogue,Shudderwock Shaman,Odd Warrior",
        "Mill Druid,Deathrattle Hunter,Big Spell Mage,Odd Warrior",
        "Mill Druid,Deathrattle Hunter,Even Shaman,Odd Warrior",
        "Malygos Druid,Deathrattle Hunter,Odd Paladin,Even Shaman",
        "Deathrattle Hunter,Even Paladin,Shudderwock Shaman,Odd Warrior",
        "Mecha'thun Druid,Secret Hunter,Big Spell Mage,Odd Warrior",
        "Even Paladin,Quest Rogue,Shudderwock Shaman,Odd Warrior",
        "Malygos Druid,Odd Paladin,Odd Rogue,Even Shaman",
        "Mill Druid,Even Paladin,Even Shaman,Big Spell Mage",
        "Malygos Druid,Even Paladin,Kingsbane Rogue,Odd Warrior",
        "Token Druid,Deathrattle Hunter,Even Paladin,Even Warlock",
        "Mill Druid,Control Priest,Big Spell Mage,Cube Warlock",
        "Token Druid,Deathrattle Hunter,Odd Paladin,Shudderwock Shaman",
        "Taunt Druid,Deathrattle Hunter,Odd Paladin,Even Warlock",
        "Malygos Druid,Deathrattle Hunter,Even Warlock,Odd Warrior",
        "Token Druid,Deathrattle Hunter,Even Paladin,Even Warlock",
        "Malygos Druid,Deathrattle Hunter,Shudderwock Shaman,Even Warlock",
        "Odd Hunter,Odd Paladin,Shudderwock Shaman,Zoo Warlock",
        "Malygos Druid,Deathrattle Hunter,Even Warlock,Odd Warrior",
        "Token Druid,Deathrattle Hunter,Murloc Mage,Even Paladin",
        "Malygos Druid,Even Paladin,Shudderwock Shaman,Odd Warrior",
        "Malygos Druid,Odd Paladin,Mecha'thun Priest,Shudderwock Shaman",
        "Deathrattle Hunter,Even Shaman,Big Spell Mage,Cube Warlock",
        "Taunt Druid,Deathrattle Hunter,Odd Paladin,Even Warlock",
        "Malygos Druid,Deathrattle Hunter,Odd Paladin,Even Warlock",
        "Malygos Druid,Spell Hunter,Odd Paladin,Zoo Warlock",
        "Malygos Druid,Deathrattle Hunter,Shudderwock Shaman,Even Warlock",
        "Malygos Druid,Odd Paladin,Mecha'thun Priest,Shudderwock Shaman",
        "Malygos Druid,Deathrattle Hunter,Even Warlock,Odd Warrior",
        "Odd Paladin,Odd Rogue,Even Shaman,Zoo Warlock",
        "Mill Druid,Combo Priest,Shudderwock Shaman,Odd Warrior",
        "Deathrattle Hunter,Odd Paladin,Odd Rogue,Even Warlock",
        "Deathrattle Hunter,Quest Rogue,Shudderwock Shaman,Control Warlock",
        "Malygos Druid,Deathrattle Hunter,Even Paladin,Odd Rogue",
        "Mill Druid,Deathrattle Hunter,Even Paladin,Even Warlock",
        "Mill Druid,Deathrattle Hunter,Resurrect Priest,Odd Warrior",
        "Odd Paladin,Odd Rogue,Even Shaman,Even Warlock",
        "Taunt Druid,Shudderwock Shaman,Even Warlock,Odd Warrior",
        "Mill Druid,Murloc Mage,Shudderwock Shaman,Odd Warrior",
        "Token Druid,Deathrattle Hunter,Even Warlock,Odd Warrior",
        "Malygos Druid,Deathrattle Hunter,Even Paladin,Even Warlock",
        "Even Paladin,Quest Rogue,Shudderwock Shaman,Odd Warrior",
        "Deathrattle Hunter,Even Paladin,Odd Rogue,Even Warlock",
        "Token Druid,Even Paladin,Odd Rogue,Even Warlock",
        "Deathrattle Hunter,Even Paladin,Even Shaman,Even Warlock",
        "Deathrattle Hunter,Even Paladin,Even Shaman,Odd Warrior",
        "Malygos Druid,Deathrattle Hunter,Odd Paladin,Odd Rogue",
        "Token Druid,Deathrattle Hunter,Even Paladin,Even Warlock",
        "Deathrattle Hunter,Even Paladin,Shudderwock Shaman,Cube Warlock",
        "Malygos Druid,Odd Paladin,Odd Rogue,Even Shaman",
        "Malygos Druid,Deathrattle Hunter,Even Paladin,Even Warlock",
        "Token Druid,Deathrattle Hunter,Murloc Mage,Odd Paladin",
        "Taunt Druid,Odd Paladin,Shudderwock Shaman,Cube Warlock",
        "Mill Druid,Deathrattle Hunter,Odd Paladin,Odd Rogue",
        "Malygos Druid,Deathrattle Hunter,Shudderwock Shaman,Odd Warrior",
        "Mill Druid,Deathrattle Hunter,Even Paladin,Odd Warrior",
        "Mill Druid,Deathrattle Hunter,Odd Paladin,Odd Rogue",
        "Malygos Druid,Deathrattle Hunter,Shudderwock Shaman,Even Warlock",
        "Malygos Druid,Deathrattle Hunter,Shudderwock Shaman,Even Warlock",
        "Secret Hunter,Even Paladin,Big Spell Mage,Odd Warrior",
        "Big Druid,Deathrattle Hunter,Even Paladin,Odd Warrior",
        "Token Druid,Deathrattle Hunter,Odd Paladin,Even Warlock",
        "Malygos Druid,Deathrattle Hunter,Even Warlock,Control Warrior",
        "Mill Druid,Quest Rogue,Cube Warlock,Odd Warrior",
        "Mill Druid,Deathrattle Hunter,Shudderwock Shaman,Odd Warrior",
        "Mill Druid,Quest Rogue,Cube Warlock,Odd Warrior",
        "Token Druid,Odd Paladin,Zoo Warlock,Odd Warrior",
        "Token Druid,Deathrattle Hunter,Even Paladin,Even Warlock",
        "Token Druid,Odd Hunter,Odd Paladin,Zoo Warlock",
        "Malygos Druid,Deathrattle Hunter,Odd Rogue,Zoo Warlock",
        "Mill Druid,Deathrattle Hunter,Murloc Mage,Odd Paladin",
        "Even Paladin,Odd Rogue,Even Shaman,Zoo Warlock",
        "Mill Druid,Odd Rogue,Cube Warlock,Odd Warrior",
        "Malygos Druid,Deathrattle Hunter,Shudderwock Shaman,Zoo Warlock",
        "Malygos Druid,Deathrattle Hunter,Odd Rogue,Zoo Warlock",
        "Taunt Druid,Turvy OTK Priest,Odd Rogue,Odd Warrior",
        "Token Druid,Odd Paladin,Cube Warlock,Odd Warrior",
        "Malygos Druid,Deathrattle Hunter,Odd Paladin,Shudderwock Shaman",
        "Taunt Druid,Deathrattle Hunter,Odd Rogue,Shudderwock Shaman",
        "Malygos Druid,Odd Paladin,Odd Rogue,Zoo Warlock",
        "Deathrattle Paladin,Shudderwock Shaman,Zoo Warlock,Odd Warrior",
        "Deathrattle Hunter,Even Paladin,Odd Rogue,Even Warlock",
        "Token Druid,Deathrattle Hunter,Even Paladin,Shudderwock Shaman",
        "Mill Druid,Deathrattle Hunter,Odd Paladin,Zoo Warlock",
        "Malygos Druid,Spell Hunter,Even Paladin,Even Warlock",
        "Malygos Druid,Deathrattle Hunter,Even Paladin,Even Warlock",
        "Malygos Druid,Deathrattle Hunter,Even Paladin,Big Spell Mage",
        "Malygos Druid,Deathrattle Hunter,Tempo Mage,Zoo Warlock",
        "Malygos Druid,Deathrattle Hunter,Odd Paladin,Even Warlock",
        "Even Paladin,Odd Rogue,Shudderwock Shaman,Even Warlock",
        "Token Druid,Deathrattle Hunter,Even Paladin,Even Shaman",
        "Mill Druid,Deathrattle Hunter,Odd Paladin,Shudderwock Shaman",
        "Quest Druid,Quest Mage,Mecha'thun Quest Priest,Mecha'thun Warlock",
        "OTK DK Paladin,Quest Druid,Odd Rogue,Shudderwock Shaman",
        "Deathrattle Hunter,Even Paladin,Shudderwock Shaman,Even Warlock",
        "Mill Druid,Deathrattle Hunter,Odd Paladin,Even Warlock",
        "Even Paladin,Quest Rogue,Shudderwock Shaman,Odd Warrior",
        "Malygos Druid,Deathrattle Hunter,Even Warlock,Odd Warrior",
        "Malygos Druid,Deathrattle Hunter,Shudderwock Shaman,Even Warlock",
        "Malygos Druid,Odd Paladin,Shudderwock Shaman,Even Warlock",
        "Odd Paladin,Even Shaman,Big Spell Mage,Odd Warrior",
        "Token Druid,Deathrattle Hunter,Odd Rogue,Even Warlock",
        "Malygos Druid,Odd Rogue,Even Warlock,Odd Warrior",
        "Mill Druid,Deathrattle Hunter,Quest Rogue,Shudderwock Shaman",
        "Deathrattle Hunter,Even Paladin,Odd Rogue,Big Spell Mage",
        "Deathrattle Hunter,Even Paladin,Odd Rogue,Big Spell Mage",
        "Malygos Druid,Even Paladin,Kingsbane Rogue,Odd Warrior",
        "Malygos Druid,Deathrattle Hunter,Odd Rogue,Control Warrior",
        "Token Druid,Deathrattle Hunter,Odd Rogue,Even Warlock",
        "Mill Druid,Deathrattle Hunter,Even Paladin,Odd Warrior",
        "Odd Paladin,Odd Rogue,Zoo Warlock,Odd Warrior",
        "Malygos Druid,Deathrattle Hunter,Odd Paladin,Even Warlock",
        "Deathrattle Hunter,Quest Rogue,Even Shaman,Even Warlock",
        "Token Druid,Deathrattle Hunter,Even Paladin,Even Warlock",
        "Odd Rogue,Shudderwock Shaman,Even Warlock,Odd Warrior",
        "Token Druid,Big Spell Mage,Cube Warlock,Odd Warrior",
        "Token Druid,Deathrattle Hunter,Even Paladin,Even Warlock",
        "Malygos Druid,Deathrattle Hunter,Zoo Warlock,Odd Warrior",
        "Mill Druid,Deathrattle Hunter,Shudderwock Shaman,Even Warlock",
        "Token Druid,Deathrattle Hunter,Even Paladin,Zoo Warlock",
        "Mill Druid,Deathrattle Hunter,Even Paladin,Odd Warrior",
        "Deathrattle Hunter,Even Paladin,Even Shaman,Even Warlock",
        "Malygos Druid,Deathrattle Hunter,Shudderwock Shaman,Control Warrior",
        "Odd Paladin,Odd Rogue,Big Spell Mage,Even Warlock",
        "Token Druid,Secret Hunter,Odd Paladin,Zoo Warlock",
        "Deathrattle Hunter,Even Paladin,Combo Priest,Even Warlock",
        "Mill Druid,Odd Paladin,Shudderwock Shaman,Even Warlock",
        "Odd Paladin,Odd Rogue,Even Shaman,Even Warlock",
        "Malygos Druid,Deathrattle Hunter,Odd Paladin,Resurrect Priest",
        "Malygos Druid,Deathrattle Hunter,Odd Paladin,Resurrect Priest",
        "Token Druid,Secret Hunter,Odd Rogue,Zoo Warlock",
        "Malygos Druid,Deathrattle Hunter,Odd Paladin,Even Warlock",
        "Deathrattle Hunter,Odd Rogue,Shudderwock Shaman,Even Warlock",
        "Token Druid,Deathrattle Hunter,Even Warlock,Odd Warrior",
        "Mill Druid,Even Paladin,Even Warlock,Odd Warrior",
        "Taunt Druid,Even Paladin,Even Warlock,Control Warrior",
        "Deathrattle Hunter,Even Paladin,Odd Rogue,Even Warlock",
        "Mill Druid,Spell Hunter,Odd Paladin,Shudderwock Shaman",
        "Resurrect Priest,Even Shaman,Big Spell Mage,Even Warlock",
        "Deathrattle Hunter,Even Paladin,Shudderwock Shaman,Even Warlock",
        "Deathrattle Hunter,Even Paladin,Odd Rogue,Even Warlock",
        "Malygos Druid,Deathrattle Hunter,Odd Paladin,Odd Rogue",
        "Deathrattle Hunter,Even Paladin,Odd Rogue,Even Warlock",
        "Malygos Druid,Deathrattle Hunter,Even Paladin,Odd Warrior",
        "Token Druid,Deathrattle Hunter,Even Shaman,Even Warlock",
        "Malygos Druid,Deathrattle Hunter,Even Paladin,Even Warlock",
        "Mill Druid,Deathrattle Hunter,Shudderwock Shaman,Odd Warrior",
        "Token Druid,Deathrattle Hunter,Shudderwock Shaman,Odd Warrior",
        "Malygos Druid,Murloc Mage,Shudderwock Shaman,Odd Warrior",
        "Spiteful Druid,Deathrattle Hunter,Shudderwock Shaman,Even Warlock",
        "Deathrattle Hunter,Even Paladin,Odd Rogue,Even Warlock",
        "Malygos Druid,Deathrattle Hunter,Even Paladin,Even Shaman",
        "Malygos Druid,Deathrattle Hunter,Shudderwock Shaman,Odd Warrior",
        "Token Druid,Deathrattle Hunter,Odd Paladin,Odd Warrior",
        "Deathrattle Hunter,Even Paladin,Odd Rogue,Even Warlock",
        "Malygos Druid,Deathrattle Hunter,Odd Paladin,Even Warlock",
        "Deathrattle Hunter,Even Paladin,Odd Rogue,Even Warlock",
        "Malygos Druid,Odd Hunter,Control Priest,Odd Rogue",
        "Token Druid,Deathrattle Hunter,Odd Paladin,Shudderwock Shaman",
        "Even Paladin,Resurrect Priest,Even Shaman,Big Spell Mage",
        "Malygos Druid,Odd Paladin,Mecha'thun Priest,Shudderwock Shaman",
        "Malygos Druid,Deathrattle Hunter,Odd Paladin,Cube Warlock",
        "Odd Paladin,Quest Rogue,Shudderwock Shaman,Big Spell Mage",
        "Malygos Druid,Odd Quest Warrior,Shudderwock Shaman,Even Warlock",
        "Mill Druid,Deathrattle Hunter,Murloc Mage,Deathrattle Paladin",
        "Taunt Druid,Deathrattle Hunter,Zoo Warlock,Odd Warrior",
        "Mill Druid,Odd Rogue,Zoo Warlock,Odd Warrior",
        "Malygos Druid,Deathrattle Hunter,Murloc Mage,Zoo Warlock",
        "Taunt Druid,Deathrattle Hunter,Shudderwock Shaman,Zoo Warlock",
        "Deathrattle Hunter,Odd Paladin,Odd Rogue,Shudderwock Shaman",
        "Mill Druid,Combo Priest,Shudderwock Shaman,Cube Warlock",
        "Mill Druid,Quest Rogue,Cube Warlock,Odd Warrior",
        "Mill Druid,Deathrattle Hunter,Odd Paladin,Odd Rogue",
        "Mill Druid,Control Priest,Odd Rogue,Even Warlock",
        "Malygos Druid,Odd Paladin,Shudderwock Shaman,Cube Warlock",
        "Malygos Druid,Resurrect Priest,Even Warlock,Odd Warrior",
        "Taunt Druid,Odd Rogue,Big Spell Mage,Even Warlock",
        "Resurrect Priest,Odd Rogue,Shudderwock Shaman,Even Warlock",
        "Malygos Druid,Deathrattle Hunter,Odd Paladin,Even Warlock",
        "Malygos Druid,Deathrattle Paladin,Even Shaman,Even Warlock",
        "Malygos Druid,Deathrattle Hunter,Odd Paladin,Odd Rogue",
        "Secret Hunter,Odd Paladin,Big Spell Mage,Even Warlock",
        "Token Druid,Deathrattle Hunter,Odd Paladin,Even Warlock",
        "Taunt Druid,Deathrattle Hunter,Odd Paladin,Zoo Warlock",
        "Token Druid,Deathrattle Hunter,Odd Paladin,Quest Rogue",
        "Odd Hunter,Odd Paladin,Shudderwock Shaman,Even Warlock",
        "Malygos Druid,Deathrattle Hunter,Odd Paladin,Even Warlock",
        "Mill Druid,Deathrattle Hunter,Even Warlock,Odd Warrior",
        #"Malygos Druid,Odd Paladin,Shudderwock Shaman,Mecha'thun Priest",
        #"Malygos Druid,Odd Paladin,Zoo Warlock,Secret Hunter",
        #"Clone Priest,Shudderwock Shaman,Malygos Druid,Odd Paladin",
        #"Malygos Druid,Odd Rogue,Shudderwock Shaman,Even Warlock", #Teebs
        #"Malygos Druid,Deathrattle Hunter,Odd Rogue,Shudderwock Shaman", #Luker
        #"Malygos Druid,Even Paladin,Even Warlock,Odd Warrior", #shoop
        #"Taunt Druid,Deathrattle Hunter,Shudderwock Shaman,Big Spell Mage", #Fenom
        #"Token Druid,Odd Paladin,Odd Rogue,Zoo Warlock", #Nikolajhoej
        #"Taunt Druid,Quest Rogue,Even Shaman,Cube Warlock", #Unlikelyhero
        #"Taunt Druid,Tempo Mage,Quest Rogue,Even Warlock", #Wrath of Cong
        #"Secret Hunter,Tempo Mage,Odd Rogue,Zoo Warlock", #mrgramman
        #"Malygos Druid,Odd Rogue,Shudderwock Shaman,Zoo Warlock", #Nef
        #"Deathrattle Hunter,Odd Paladin,Odd Rogue,Zoo Warlock", #Vandoom
        #"Malygos Druid,Deathrattle Hunter,Odd Rogue,Even Warlock", #KissyCat
        #"Taunt Druid,Deathrattle Hunter,Quest Rogue,Cube Warlock", #Sequinox
        #"Malygos Druid,Odd Paladin,Odd Rogue,Zoo Warlock", #EzekieL
        #"Malygos Druid,Deathrattle Hunter,Odd Paladin,Zoo Warlock", #rayC
        #"Taunt Druid,Control Priest,Miracle Rogue,Even Warlock", #korextron
        #"Token Druid,Odd Paladin,Odd Rogue,Zoo Warlock", #Hoej
        #"Malygos Druid,Deathrattle Hunter,Odd Rogue,Even Warlock", #Snowy
        #"Odd Paladin,Odd Rogue,Even Shaman,Zoo Warlock", #bLAKERS
        #"Mill Druid,Deathrattle Hunter,Odd Paladin,Zoo Warlock", #DanZack
        #"Token Druid,Odd Rogue,Even Shaman,Zoo Warlock", #Deep3
        #"Murloc Mage,Odd Paladin,Odd Rogue,Even Warlock", #Veeduh
        #"Deathrattle Hunter,Odd Paladin,Shudderwock Shaman,Even Warlock", #TheIOvOI
        #"Malygos Druid,Odd Paladin,Odd Rogue,Zoo Warlock", #Guu
        #"Mill Druid,Deathrattle Hunter,Shudderwock Shaman,Even Warlock", #Broshy
        #"Malygos Druid,Deathrattle Hunter,Shudderwock Shaman,Even Warlock", #tyler
        #"Malygos Druid,Deathrattle Hunter,Shudderwock Shaman,Even Warlock", #kuonet
        #"Malygos Druid,Deathrattle Hunter,Shudderwock Shaman,Even Warlock", #Roger
        #"Malygos Druid,Deathrattle Hunter,Shudderwock Shaman,Even Warlock", #Mitsuhide
        #"Token Druid,Odd Paladin,Shudderwock Shaman,Odd Warrior", #killinallday
        #"Malygos Druid,Deathrattle Hunter,Odd Rogue,Even Warlock", #Innovation
        #"Token Druid,Odd Paladin,Shudderwock Shaman,Odd Warrior", #DrJikininki
        #"Token Druid,Even Shaman,Big Spell Mage,Even Warlock", #Deus
        #"Malygos Druid,Secret Hunter,Odd Paladin,Odd Warrior", #Bacon
        #"Token Druid,Odd Paladin,Shudderwock Shaman,Odd Warrior", #Ant
        #"Mill Druid,Deathrattle Hunter,Quest Rogue,Cube Warlock", #Envoy
        #"Taunt Druid,Deathrattle Hunter,Resurrect Priest,Quest Rogue", #Rage
        #"Murloc Mage,Odd Paladin,Odd Rogue,Zoo Warlock", #D22soso
        #"Taunt Druid,Deathrattle Hunter,Odd Paladin,Even Warlock", #Emitong
        #"Taunt Druid,Deathrattle Hunter,Odd Rogue,Shudderwock Shaman", #vandit
        #"Taunt Druid,Deathrattle Hunter,Combo Priest,Even Warlock", #Crane333
        #"Malygos Druid,Deathrattle Hunter,Shudderwock Shaman,Even Warlock", #Perna
        #"Taunt Druid,Odd Rogue,Even Shaman,Even Warlock", #hypnotoxic
        #"Malygos Druid,Combo Priest,Even Shaman,Even Warlock", #Beegan
        #"Mill Druid,Deathrattle Hunter,Shudderwock Shaman,Even Warlock", #ETC
        #"Malygos Druid,Deathrattle Hunter,Deathrattle Paladin,Cube Warlock", #TheChosenGuy
        #"Malygos Druid,Control Priest,Odd Rogue,Shudderwock Shaman", #Toastmonster
        #"Malygos Druid,Deathrattle Hunter,Shudderwock Shaman,Even Warlock", #AKAWonder
        #"Token Druid,Odd Paladin,Shudderwock Shaman,Odd Warrior", #SwaggyG
        #"Malygos Druid,Deathrattle Hunter,Odd Rogue,Even Warlock", #YuNicorn
        #"Odd Paladin,Odd Rogue,Shudderwock Shaman,Cube Warlock", #GETNIT
        #"Taunt Druid,Deathrattle Hunter,Deathrattle Paladin,Cube Warlock", #jakaso27
        #"Malygos Druid,Deathrattle Hunter,Resurrect Priest,Even Warlock", #AppsCaramel
        #"Malygos Druid,Deathrattle Hunter,Odd Paladin,Odd Rogue", #Justsaiyan
        #"Taunt Druid,Deathrattle Hunter,Quest Rogue,Cube Warlock", #katsucurry
        #"Malygos Druid,Deathrattle Hunter,Odd Paladin,Even Warlock", #Tyfoon
        #"Malygos Druid,Deathrattle Hunter,Shudderwock Shaman,Even Warlock", #Seiko
        #"Malygos Druid,Deathrattle Hunter,Shudderwock Shaman,Odd Warrior", #jinsoo
        #"Token Druid,Murloc Mage,Odd Paladin,Even Shaman", #SamuelTsao
        #"Quest Druid,Deathrattle Hunter,Combo Priest,Quest Rogue", #SmokedSalmon
        #"Malygos Druid,Deathrattle Hunter,Odd Rogue,Shudderwock Shaman", #Ryder
        #"Deathrattle Hunter,Odd Rogue,Shudderwock Shaman,Odd Warrior", #ntR
        #"Malygos Druid,Deathrattle Hunter,Shudderwock Shaman,Cube Warlock", #Jarla
        #"Taunt Druid,Deathrattle Hunter,Deathrattle Paladin,Shudderwock Shaman", #seohyun628
        #"Malygos Druid,Odd Paladin,Odd Rogue,Zoo Warlock", #Tarei
        #"Malygos Druid,Shudderwock Shaman,Cube Warlock,Odd Warrior", #Flamekilla
        #"Malygos Druid,Deathrattle Hunter,Odd Paladin,Odd Rogue", #Villain
        #"Token Druid,Deathrattle Hunter,Odd Rogue,Zoo Warlock", #StormFever
        #"Malygos Druid,Deathrattle Hunter,Shudderwock Shaman,Even Warlock", #Dalesom
        #"Malygos Druid,Deathrattle Hunter,Odd Rogue,Zoo Warlock", #Gallon
        #"Malygos Druid,Deathrattle Hunter,Odd Paladin,Odd Rogue", #Akumaker
        #"Odd Paladin,Odd Rogue,Even Shaman,Zoo Warlock", #Xixo
        #"Mill Druid,Odd Paladin,Shudderwock Shaman,Odd Warrior", #Sol
        #"Secret Hunter,Odd Paladin,Odd Rogue,Zoo Warlock", #HearthDad
        #"Taunt Druid,Spell Hunter,Shudderwock Shaman,Odd Warrior", #hatul
        #"Token Druid,Deathrattle Hunter,Shudderwock Shaman,Even Warlock", #rosty
        #"Malygos Druid,Deathrattle Hunter,Shudderwock Shaman,Even Warlock", #Rase
        #"Malygos Druid,Deathrattle Hunter,Shudderwock Shaman,Cube Warlock", #pnc
        #"Malygos Druid,Deathrattle Hunter,Odd Rogue,Shudderwock Shaman", #Qwerty97
        #"Secret Hunter,Odd Paladin,Odd Rogue,Even Shaman", #Insom
        #"Token Druid,Odd Paladin,Even Shaman,Zoo Warlock", #Lii
        #"Mill Druid,Even Paladin,Even Warlock,Odd Warrior", #Triton
        #"Token Druid,Odd Paladin,Odd Rogue,Even Shaman", #Alan870806
        #"Malygos Druid,Deathrattle Hunter,Odd Paladin,Cube Warlock", #Butterz
        #"Malygos Druid,Deathrattle Hunter,Shudderwock Shaman,Even Warlock", #Cydonia
        #"Malygos Druid,Deathrattle Hunter,Odd Rogue,Zoo Warlock", #purple
        #"Malygos Druid,Deathrattle Hunter,Odd Paladin,Odd Rogue", #GreenSheep
        #"Malygos Druid,Quest Rogue,Shudderwock Shaman,Cube Warlock", #bobbyex
        #"Malygos Druid,Deathrattle Hunter,Odd Rogue,Shudderwock Shaman", #Ostkaka
        #"Token Druid,Deathrattle Hunter,Odd Paladin,Cube Warlock", #BoarControl
        #"Token Druid,Odd Paladin,Odd Rogue,Even Shaman", #Amnesiac
        #"Malygos Druid,Deathrattle Hunter,Odd Rogue,Shudderwock Shaman", #Muzzy
        #"Malygos Druid,Deathrattle Hunter,Combo Priest,Even Warlock", #N0lan
        #"Token Druid,Deathrattle Hunter,Odd Paladin,Odd Rogue", #SoLegit
        #"Malygos Druid,Deathrattle Hunter,Shudderwock Shaman,Even Warlock", #Bozzzton
        #"Malygos Druid,Deathrattle Hunter,Murloc Mage,Odd Rogue", #Monsanto
        #"Malygos Druid,Odd Paladin,Odd Rogue,Shudderwock Shaman", #Hunterace
        #"Malygos Druid,Odd Paladin,Odd Rogue,Shudderwock Shaman", #MegaManMusic
        #"Malygos Druid,Deathrattle Hunter,Shudderwock Shaman,Even Warlock", #casie
        #"Malygos Druid,Deathrattle Hunter,Even Warlock,Control Warrior", #Swidz
        #"Malygos Druid,Deathrattle Hunter,Odd Paladin,Odd Rogue", #impact
        #"Token Druid,Deathrattle Hunter,Odd Paladin,Cube Warlock", #Fenomeno
    ]
    lineups_to_test = [l.split(',') for l in lineups_to_test]
    weights = [1 for l in lineups_to_test if l is not None]
    #weights = [5,5,4,4,3,3,3,3,3,2,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    #weights = [11, 6, 4, 4, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

    import sys
    args = sys.argv[1:]
    if len(args) > 0 and args[0] == 'practice':
        win_pcts, num_games, game_count, archetypes, overall_wr = get_win_pcts(min_game_threshold=0, min_game_count=0,limitTop=100)
        overrides = [
        ]
        win_pcts = override_wr(overrides,win_pcts)
        
        my_lineup = [d.strip() for d in args[1].split(',')]
        #opp_lineup = [d.strip() for d in deck_2.split(',')]
        total, count = 0.0, 0
        bans = {}
        values = []
        for opp_lineup, weight in zip(lineups_to_test, weights):
            assert all([d in archetypes for d in my_lineup]), ([d in archetypes for d in my_lineup], my_lineup)
            assert all([d in archetypes for d in opp_lineup]), ([d in archetypes for d in opp_lineup], opp_lineup)
            ban, win_pct = win_rate(my_lineup, opp_lineup, win_pcts)
            bans[ban] = bans.get(ban, 0) + 1
            print ",".join([str(i) for i in [opp_lineup, ban, win_pct]])
            wr =  win_rate(my_lineup, opp_lineup, win_pcts)
            if win_pct > 0:
                count += weight
                total += win_pct * weight
                values.append(win_pct)
            print wr
            #print pre_ban(my_lineup, opp_lineup, win_pcts)
            print pre_ban_nash_calc(my_lineup, opp_lineup, win_pcts)
            # BAN STUFF
            showBans = False
            if showBans:
                print my_lineup, "vs", opp_lineup
                win_rates_grid(my_lineup, opp_lineup, win_pcts, num_games)
                res = pre_ban_old(my_lineup,
                                  opp_lineup,
                                  win_pcts)
                print ""
                print my_lineup, "vs", opp_lineup
                print "bans"
                print "%-20s %-20s" % ("p1_ban", "p2_ban")
                #for i, j in sorted(res.items(), key=lambda x:-x[1]):
                for i, j in sorted(res.items(), key=lambda x:(x[0][0], x[1])):
                    d1, d2 = i
                    print '%-20s %-20s %s' % (d1, d2, round(j,4))
                print "\n\n"
        print("average: %s" % (total /count))
        print("min: %s" % min(values))
        print("bans: %s" % sorted(bans.items(), key=lambda x:x[1], reverse=True))
    elif len(args) > 0 and args[0] == 'sim':
        win_pcts, num_games, game_count, archetypes, overall_wr = get_win_pcts(min_game_threshold=0, min_game_count=0)
        print len(archetypes), sorted(archetypes, key=class_sort)
        my_lineup = [d.strip() for d in args[1].split(',')]
        opp_lineup = [d.strip() for d in args[2].split(',')]
        assert all([d in archetypes for d in my_lineup]), ([d in archetypes for d in my_lineup], my_lineup)
        assert all([d in archetypes for d in opp_lineup]), ([d in archetypes for d in opp_lineup], opp_lineup)

        if len(my_lineup) == 4:

            print my_lineup, "vs", opp_lineup
            win_rates_grid(my_lineup, opp_lineup, win_pcts, num_games)
            #print win_rate(my_lineup, opp_lineup, win_pcts)
            print round(pre_ban_nash_calc(my_lineup, opp_lineup, win_pcts), 4)
            print "BANS",pre_ban_nash(my_lineup, opp_lineup, win_pcts)
            print pre_ban(my_lineup, opp_lineup, win_pcts)

            print '\nOPP BANS'
            print win_rate(opp_lineup, my_lineup, win_pcts)
            print pre_ban(opp_lineup,my_lineup,win_pcts)

            res = pre_matrix(my_lineup,
                             opp_lineup,
                             win_pcts)
            print ""
            print my_lineup, "vs", opp_lineup
            print "bans"
            print "%-27s %-27s" % ("p1_ban", "p2_ban")
            #for i, j in sorted(res.items(), key=lambda x:-x[1]):
            for i, j in sorted(res.items(), key=lambda x:(x[0][0], x[1])):
                d1, d2 = i
                print '%-27s %-27s %s' % (d1, d2, round(j,4))
            print "bans"
            print "%-27s %-27s" % ("p1_ban", "p2_ban")
            for i, j in sorted(res.items(), key=lambda x:(x[0][1], x[1])):
                d1, d2 = i
                print '%-27s %-27s %s' % (d1, d2, round(j,4))
        elif len(my_lineup) <= 3:
            print my_lineup, "vs", opp_lineup
            win_rates_grid(my_lineup, opp_lineup, win_pcts, num_games)
            #print win_rate(my_lineup, opp_lineup, win_pcts)
            #print pre_ban(my_lineup, opp_lineup, win_pcts)

            res, matrix = lead_matrix(my_lineup,
                                      opp_lineup,
                                      win_pcts)
            print ""
            print my_lineup, "vs", opp_lineup
            print "leads"
            print "%-27s %-27s" % ("p1_lead", "p2_lead")
            #for i, j in sorted(res.items(), key=lambda x:-x[1]):
            for i, j in sorted(res.items(), key=lambda x:(x[0][1], -x[1])):
                d1, d2 = i
                print '%-27s %-27s %s' % (d1, d2, round(j,4))
            
    else:
        win_pcts, num_games, game_count, archetypes, overall_wr = get_win_pcts(min_game_threshold=40, min_game_count=20, min_win_pct=0.44,limitTop=35)
        if True:
            filename = 'hct_atl.csv'
            #win_pcts2, archetypes2 = wr_from_csv(filename, scaling=100)
            win_pcts2, archetypes = wr_from_csv(filename, scaling=100)
            win_pcts.update(win_pcts2)
        overrides = [
            #('Quest Rogue', 'Zoo Warlock', 0.5),
            #('Quest Rogue', 'Odd Rogue', 0.5),
        ]
        win_pcts = override_wr(overrides,win_pcts)
        print len(archetypes), sorted(archetypes, key=class_sort)

        excluded = []
        excluded += ["Mecha'thun Priest"]
        excluded += ['Quest Rogue']
        #excluded = ['Spiteful Druid', 'Spiteful Priest', 'Miracle Rogue', 'Pirate Warrior']
        #excluded = ['Aggro Hunter', 'Combo Priest', 'Rush Warrior', 'Odd Hunter', 'Odd Paladin']
        #excluded = ['Odd Paladin', 'Cube Warlock', 'Control Warlock']
        print "\n\nEXCLUDING:", excluded
        archetypes = [a for a in archetypes if a not in excluded]

        additional_archetypes = []
        for lu_test in lineups_to_test:
            for a in lu_test:
                if a not in archetypes:
                    print("Rare Archetypes: %s" % a)
                    additional_archetypes.append(a)
        lineups, archetype_map = generate_lineups(archetypes, additional_archetypes=additional_archetypes, num_classes=4)
        inverse_map = {}
        for i,j in archetype_map.items():
            inverse_map[j] = i
        win_pcts_int = {}
        for i,a in archetype_map.items():
            for j,b in archetype_map.items():
                if (a,b) in win_pcts:
                    win_pcts_int[(i,j)] = win_pcts[(a,b)]

        print "testing %s lineups" % len(lineups)

        win_rates_against_good = {}

        if len(args) > 0 and args[0] == 'target':
            lineups_to_test = []
            for x in args[1:]:
                tmp = [i.strip() for i in x.split(',')]
                lineups_to_test.append(tmp)
            weights = [1 for i in lineups_to_test]
        #if len(args) > 0 and args[0] == 'target':
        #    level1 = [i.strip() for i in args[1].split(',')]
        #    weights = [1]
        #    lineups_to_test = [level1]
        print "\n"
        print "TESTING vs LINEUPS"
        for l in lineups_to_test:
            print '"' + ",".join(l) + '"'
        print "\n"

        for lineup in lineups:
            for lu_test in lineups_to_test:
                lu_test = list(get_lineup(lu_test, inverse_map))
                win_rates_against_good[lineup] = win_rates_against_good.get(lineup, []) + [win_rate(list(lineup), lu_test, win_pcts_int, useGlobal=True)]
                #win_rates_against_good[lineup] = win_rates_against_good.get(lineup, []) + [pre_ban_nash_calc(list(lineup), lu_test, win_pcts_int, useGlobal=True)]

        lu_strings = []
        #for i,j in sorted(win_rates_against_good.items(), key=lambda x:sum([i[1] for i in x[1]]))[-10:]:
        #for i,j in sorted(win_rates_against_good.items(), key=lambda x:min([i[1] for i in x[1]]))[-10:]:
        #for i,j in sorted(win_rates_against_good.items(), key=lambda x:geometric_mean([i[1] for i in x[1]],weights))[-10:]:
        #for i,j in sorted(win_rates_against_good.items(), key=lambda x:sumproduct_normalize([i[1] for i in x[1]],weights) * 3 + min([i[1] for i in x[1]]))[-10:]:
        #for i,j in sorted(win_rates_against_good.items(), key=lambda x:sumproduct_normalize([i[1] for i in x[1]],weights) * 3 + min([i[1] for i in x[1]]))[-40:]:
        final = sorted(win_rates_against_good.items(), key=lambda x:sumproduct_normalize([i[1] for i in x[1]],weights))
        usingFilter = False
        if usingFilter:
            tmp = []
            for x, y in final:
                if 'Shudderwock Shaman' in get_lineup(x, archetype_map) and 'Quest Rogue' in get_lineup(x, archetype_map):
                    tmp.append((x, y))
            final = tmp
        for i,j in final[-40:]:
            tmp = []
            for x in j:
                tmp_sub = tuple([archetype_map[x[0]]] + list(x[1:]))
                tmp.append(tmp_sub)
            j = tmp
            i = get_lineup(i, archetype_map)
            i_print = "    " + "".join(["%-20s" % x for x in i])
            #print "%-80s %s %s" % (i_print,j, round(sum([x[1] for x in j])/len(j),3)), '"' + ",".join(i) + '"'
            print "%-80s %s %s" % (i_print,j, round(sum([x[1] for x in j])/len(j),3))
            lineup_string = ",".join(i)
            lu_strings.append((lineup_string, round(sum([x[1] for x in j])/len(j),3), round(sumproduct_normalize([i[1] for i in j],weights),3), round(min([x[1] for x in j]),3)))
            print '         "' + lineup_string + '"'
    
        for i,j,k,l in lu_strings:
            print "".join(["%-20s" % x for x in i.split(',')]), j, k, l, '    "%(i)s"' % locals()

        #    i_print = "    " + "".join(["%-27s" % x for x in i])
        #    #print "%-80s %s %s" % (i_print,j, round(sum([x[1] for x in j])/len(j),3)), '"' + ",".join(i) + '"'
        #    print "%-80s %s %s" % (i_print,j, round(sum([x[1] for x in j])/len(j),3))
        #    lineup_string = ",".join(i)
        #    lu_strings.append((lineup_string, round(sum([x[1] for x in j])/len(j),3), round(sumproduct_normalize([i[1] for i in j],weights),3),round(min([x[1] for x in j]),3)))
        #    print '         "' + lineup_string + '"'
        #for i,j,k,l in lu_strings:
        #    print "".join(["%-27s" % x for x in i.split(',')]), j, k, l
        if usingFilter:
            print("Warning, these results were filtered")
