from label_archetype import *

filename = '2018_HCT_Americas_Fall_Playoffs.csv'

file = open(filename)
lines = [line.strip().split(',') for line in file]

output = open('with_arch.csv', 'w')
archetypes = {}
a_type = {}
for p, c, d in lines[1:]:
    if p not in archetypes:
        archetypes[p] = []
    tmp = EasyDeck(d, p)
    label = label_archetype(tmp)
    if not label:
        print(p, d)
        tmp.print_deck()
    else:
        if label not in a_type: a_type[label] = []
        a_type[label].append(tmp)
        archetypes[p].append(label)
        output.write(",".join([p,c,d,label]) + '\n')

for i in archetypes:
    archetypes[i] = sorted(archetypes[i], key=lambda x:x.split(' ')[-1])

for i,j in archetypes.items():
    i = i.split('#')[0] + '"'
    p = "%-20s" % ('' + i + '')
    print('        %s : "%s",' % (p, ",".join(j)))
