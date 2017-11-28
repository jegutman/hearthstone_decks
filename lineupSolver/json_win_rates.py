import json
filename = 'hsreplay1127.json'
print "using:", filename
wr_file = open(filename)

from get_archetypes import *

def get_win_pcts(min_game_threshold=0, min_game_count=0):
    # returns win_pcts, num_games, game_count, archetypes
    win_pcts = {}
    num_games = {}
    game_count = {}
    hsreplay_archetypes = []
    #min_game_threshold = 200
    #min_game_threshold = 0
    wr_json = json.load(wr_file)
    for a1 in wr_json['series']['data'].keys():
        arch1 = get_archetype(a1.strip())
        if arch1 is None: continue
        if arch1 not in hsreplay_archetypes:
            hsreplay_archetypes.append(arch1)
            game_count[arch1] = 0
        for a2 in wr_json['series']['data'][a1].keys():
            arch2 = get_archetype(a2)
            wr, total_games = wr_json['series']['data'][a1][a2]['win_rate'], wr_json['series']['data'][a1][a2]['total_games']
            if total_games >= min_game_threshold:
                win_pcts[(arch1, arch2)] = wr / 100.
            num_games[(arch1, arch2)] = total_games
            game_count[arch1] += total_games
    hsreplay_archetypes = [a for a in hsreplay_archetypes if game_count[a] > min_game_count]
    return win_pcts, num_games, game_count, hsreplay_archetypes

if __name__ == "__main__":
    win_pcts, num_games, game_count, archetypes = get_win_pcts(min_game_threshold=200, min_game_count=100)
