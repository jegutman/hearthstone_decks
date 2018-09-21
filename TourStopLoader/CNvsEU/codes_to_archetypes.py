import sys
sys.path.append('../../')
from config import basedir
sys.path.append(basedir)
sys.path.append(basedir + '/lineupSolver')
sys.path.append('../TourStopLoader')

from json_win_rates import *
from label_archetype import label_archetype
from deck_manager import *


filename = 'CNvsEU.csv'
week_file = open(filename)
#output_file = open(filename.replace('codes', 'lineups'), 'w')
output_file = open('CNvsEUarchetypes.csv')
lines = [line.strip() for line in week_file]

output_file.write(lines[0] + '\n')
for line in lines[1:]:
    print(line)
    tmp = line.split(',')
    player = tmp[0]
    for i in tmp[1:5]:
        #print(country, i)
        label = label_archetype(EasyDeck(i))
        if not label: 
            print('x',i,'x')
            EasyDeck(i).print_deck()
    archetypes = [label_archetype(EasyDeck(i)) for i in tmp[1:10]]
    print(archetypes)
    output_file.write(",".join([country] + archetypes) + '\n')
