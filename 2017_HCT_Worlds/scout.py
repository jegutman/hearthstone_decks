import os
all_files = []
for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".txt"):
             #print(os.path.join(root, file))
             all_files.append(os.path.join(root, file))

player_archetypes = {}
for filename in all_files:
    #print filename
    tmp = filename.split('/')
    player = tmp[1]
    deck = tmp[2].split('.')[0]
    f_tmp = open(filename)
    code = None
    for line in f_tmp:
        if not code:
            code = line.strip()
    f_tmp.close()
    #print player,deck, code
    if player not in player_archetypes:
        player_archetypes[player] = []
    player_archetypes[player].append(deck)

for i,j in player_archetypes.items():
    lu_string = ",".join(j)
    i = '"' + i + '"'
    #print '%-20s : "%s",' % (i,lu_string)

for i,j in player_archetypes.items():
    lu_string = ""
    for k in j:
        lu_string += "%-30s" % k
    print "%-20s %s" % (i,lu_string)
