import random

avg_bottom = 0
total_bottom = 0
cutoff = 0.3
count = 0
for _x in range(0, 10000):
    players = [0,1,2,3,4,5,6,7]
    result = {}
    games = {}

    for i in players:
        for j in players:
            if j<= i: continue
            games[i] = games.get(i,0) + 2
            games[j] = games.get(j,0) + 2
            match = random.randint(0,1)
            result[i] = result.get(i,0) + match
            result[j] = result.get(j,0) + (1-match)
            match = random.randint(0,1)
            result[i] = result.get(i,0) + match
            result[j] = result.get(j,0) + (1-match)

    #print(min(result.values()), max(result.values()))
    avg_bottom += min(result.values()) / float(games[0])
    if min(result.values()) / float(games[0]) < cutoff:
        count += 1
    total_bottom += 1

print(avg_bottom / total_bottom)
print(count / total_bottom)
