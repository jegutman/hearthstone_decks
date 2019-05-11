file = open('season3.raw')
players = set()
for line in file:
    tmp = line.strip().split()
    if len(tmp) >= 2:
        try:
            player = tmp[0]
            pts = int(tmp[1])
        except:
            continue
        if player not in ('Americas', 'Asia-Pacific', 'Europe') and player not in players:
            players.add(player)
            print("%s,%s" % (player, pts))
