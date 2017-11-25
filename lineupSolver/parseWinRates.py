
#filename = 'vs1123_alt.csv'
filename = 'vs1123.csv'
print "using: %s" % filename

topKey = ""
count = 0

win_pcts = {}

with open(filename) as f:
    for line in f:
        tmp = line.split(',')[:-1]
        if not topKey:
            topKey = tmp
            continue
        for i in range(1, len(tmp)):
            if tmp[i].strip():
                win_pcts[(tmp[0], topKey[i])] = float(tmp[i])

#print topKey
archetypes = topKey[1:]
