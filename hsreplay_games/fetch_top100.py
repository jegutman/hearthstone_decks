import requests
import time
max_game = 1000
url = "https://hsreplay.net/api/v1/live/replay_feed/?format=json&offset=%(offset)s"
game_url = "https://hsreplay.net/api/v1/games/%(game_id)s/?format=json"
games = []
for offset in range(0, max_game, 200):
    tmp_games = requests.get(url % locals()).json()['data']
    for game in tmp_games:
        game_id = game['id']
        if game['player1_legend_rank'] == 'None': continue
        if game['player2_legend_rank'] == 'None': continue
        if int(game['player1_legend_rank']) <= 500 or int(game['player2_legend_rank']) <= 500:
            #games.append(game)
            game_info = requests.get(game_url % locals()).json()
            p1 = game_info['friendly_player']['name']
            p2 = game_info['opposing_player']['name']
            games.append([p1, p2, game])

#counts = {}
#for i,j,k in games:
#    counts[i] = counts.get(i, 0) + 1
#    counts[j] = counts.get(j, 0) + 1
#for i, j in sorted(counts.items(), key=lambda x:x[1], reverse=True):
#    print(j, i)
