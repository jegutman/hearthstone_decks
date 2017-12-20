import json
#filename = 'hsreplay1220.json'
#filename = 'hsreplay1220day.json'
filename = 'hsreplay1220legend.json'

#import datetime, os
#filename = 'hsreplay' + datetime.datetime.today().strftime("%m%d") + '.json'
#url = 'https://hsreplay.net/analytics/query/head_to_head_archetype_matchups/?GameType=RANKED_STANDARD&RankRange=ONE_THROUGH_FIVE&Region=ALL&TimeRange=LAST_7_DAYS'
#url = 'https://hsreplay.net/analytics/query/head_to_head_archetype_matchups/?GameType=RANKED_STANDARD&RankRange=ONE_THROUGH_FIVE&Region=ALL&TimeRange=LAST_3_DAYS'
#os.system('curl -o %(filename)s %(url)s' % locals())

print "using:", filename

from get_archetypes import *

def get_win_pcts(min_game_threshold=0, min_game_count=0, min_win_pct=0):
    wr_file = open(filename)
    # returns win_pcts, num_games, game_count, archetypes
    overall_wr = {}
    win_pcts = {}
    num_games = {}
    game_count = {}
    hsreplay_archetypes = []
    #min_game_threshold = 200
    #min_game_threshold = 0
    wr_json = json.load(wr_file)
    for a1 in wr_json['series']['data'].keys():
        arch1 = get_archetype(a1.strip())
        overall_wr[arch1] = wr_json['series']['metadata'][a1]['win_rate'] / 100.
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
    hsreplay_archetypes = [a for a in hsreplay_archetypes if game_count[a] > min_game_count and overall_wr[a] >= min_win_pct]
    wr_file.close()
    return win_pcts, num_games, game_count, hsreplay_archetypes, overall_wr

if __name__ == "__main__":
    win_pcts, num_games, game_count, archetypes, overall_wr = get_win_pcts(min_game_threshold=200, min_game_count=100)
