import random

def sim_game(p1, p2, y):
    if p1 != 0:
        return random.randint(0,1)
    else:
        return 1 if random.random() < y else 0
    
for y in range(20, 75, 5):
    avg_bottom = 0
    total_bottom = 0
    count = 0
    pct = y / 100.
    for _x in range(0, 10000):
        players = [0,1,2,3,4,5,6,7]
        result = {}
        games = {}

        for i in players:
            for j in players:
                if j<= i: continue
                games[i] = games.get(i,0) + 2
                games[j] = games.get(j,0) + 2
                match = sim_game(i,j, pct)
                result[i] = result.get(i,0) + match
                result[j] = result.get(j,0) + (1-match)
                match = sim_game(i,j, pct)
                result[i] = result.get(i,0) + match
                result[j] = result.get(j,0) + (1-match)

        #print(min(result.values()), max(result.values()))
        min_res = min(result.items(), key=lambda x:x[1])[1]
        #print(min_res)
        count_min = sum([1 for i in result.keys() if result[i] == min_res])
        #print(count_min)
        if result[0] == min_res:
            count += 1 / count_min
        total_bottom += 1
        #print(games[0])

    #print(avg_bottom / total_bottom)
    print("%0.2f" % pct, round(count / total_bottom, 3))
