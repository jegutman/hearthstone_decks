file = open('play_time.out')
player_starts = {}
player_ends = {}
game_time = {}
times = []
for line in file:
    player, tournament, start_time, end_time = line.strip().split(' ')
    if player not in player_starts:
        player_starts[player] = {}
        player_ends[player] = {}
    if tournament not in player_starts[player]:
        player_starts[player][tournament] = 1e100
        player_ends[player][tournament] = 0
    start_time = int(start_time)
    end_time = int(end_time)
    if end_time - start_time > 10800: end_time = start_time + 10800
    times.append((round((end_time - start_time) / 60, 2), player, tournament))
    game_time[player] = game_time.get(player, 0) + end_time - start_time
    player_starts[player][tournament] = min(player_starts[player][tournament], start_time)
    player_ends[player][tournament] = max(player_ends[player][tournament], end_time)

total_time = {}

for player in player_starts:
    total_time[player] = 0
    for tournament in player_starts[player]:
        total_time[player] += (player_ends[player][tournament] -player_starts[player][tournament])

#for i,j in sorted(total_time.items(), key=lambda x:x[1], reverse=True)[:100]:
#for i,j in sorted(game_time.items(), key=lambda x:x[1], reverse=True)[:100]:
for i,j in sorted(game_time.items(), key=lambda x:x[1], reverse=True):
    #print("%-20s %6s %6s" % (i,round(total_time[i] / 3600,1), round(game_time[i] / 3600, 1)))
    print("%s,%s,%s" % (i,round(total_time[i] / 3600,1), round(game_time[i] / 3600, 1)))

for i,j,k in sorted(times)[-40:]:
    print(i,j,k)
