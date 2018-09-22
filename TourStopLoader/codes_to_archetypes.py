import sys
sys.path.append('../')
from config import basedir
sys.path.append(basedir)
sys.path.append(basedir + '/lineupSolver')
sys.path.append('../TourStopLoader')

from json_win_rates import *
from label_archetype import label_archetype
from deck_manager import *


filename = 'wesg_codes.csv'
week_file = open(filename)
output_file = open(filename.replace('codes', 'lineups'), 'w')
lines = [line.strip() for line in week_file]

#country,Warrior,Priest,Shaman,Warlock,Paladin,Rogue,Mage,Druid,Hunter
output_file.write(lines[0] + '\n')
for line in lines[0:]:
    print(line)
    tmp = line.split(',')
    country = tmp[0]
    for i in tmp[1:]:
        #print(country, i)
        label = label_archetype(EasyDeck(i))
        if not label: 
            print('x',i,'x')
            EasyDeck(i).print_deck()
            label = "Unknown"
    archetypes = [label_archetype(EasyDeck(i), default="Unknown") for i in tmp[1:]]
    print(archetypes)
    output_file.write(",".join([country] + archetypes) + '\n')
