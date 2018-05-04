import sys
sys.path.append('../')
from config import basedir
sys.path.append(basedir)
sys.path.append(basedir + '/lineupSolver')

import json
from config import basedir

date = '20180503'
base = basedir
#filename = '%(base)slineupSolver/win_rates/hsreplay%(date)s_L5_7DAYS.json' % locals()
#filename = '%(base)slineupSolver/win_rates/hsreplay%(date)s_LONLY_1DAY.json' % locals()
#filename = '%(base)slineupSolver/win_rates/hsreplay%(date)s_LONLY_3DAYS.json' % locals()
filename = '%(base)slineupSolver/win_rates/hsreplay%(date)s_LONLY_7DAYS.json' % locals()
#filename = '%(base)slineupSolver/win_rates/hsreplay%(date)sday.json' % locals()
#filename = '%(base)slineupSolver/win_rates/hsreplay%(date)slegend_day.json' % locals()
#filename = '%(base)slineupSolver/win_rates/hsreplay%(date)slegend_day.json' % locals()
#filename = '%(base)slineupSolver/win_rates/hsreplay%(date)s_7day.json' % locals()
#filename = '%(base)slineupSolver/win_rates/hsreplay%(date)slegend7.json' % locals()

#import datetime, os
#filename = 'hsreplay' + datetime.datetime.today().strftime("%m%d") + '.json'
#url = 'https://hsreplay.net/analytics/query/head_to_head_archetype_matchups/?GameType=RANKED_STANDARD&RankRange=ONE_THROUGH_FIVE&Region=ALL&TimeRange=LAST_7_DAYS'
#url = 'https://hsreplay.net/analytics/query/head_to_head_archetype_matchups/?GameType=RANKED_STANDARD&RankRange=ONE_THROUGH_FIVE&Region=ALL&TimeRange=LAST_3_DAYS'
#os.system('curl -o %(filename)s %(url)s' % locals())

print("using:", filename)

from get_archetypes import *
from shared_utils import class_sort

def override_wr(overrides, win_pcts):
    for a, b, pct in overrides:
        win_pcts[(a,b)] = pct
        win_pcts[(b,a)] = 1 - pct
    return win_pcts

def get_win_pcts(min_game_threshold=0, min_game_count=0, min_win_pct=0, filename=filename,limitTop=1000):
    #from get_archetypes import get_archetype
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
    top_arch = sorted(game_count.keys(), key=lambda x:game_count[x], reverse=True)[:limitTop]
    hsreplay_archetypes = [a for a in hsreplay_archetypes if game_count[a] > min_game_count and overall_wr[a] >= min_win_pct and a in top_arch]
    hsreplay_archetypes.sort(key=class_sort)
    wr_file.close()
    return win_pcts, num_games, game_count, hsreplay_archetypes, overall_wr

def wr_to_csv(win_pcts, archetypes, scaling=1, default = 0.4999):
    res = []
    res.append(",".join([""] + archetypes))
    for i in archetypes:
        line = [i]
        for j in archetypes:
            line += [str(win_pcts.get((i,j), default) * scaling)]
        res.append(",".join(line))
    return "\n".join(res)

def wr_from_csv(filename, scaling=1):
    win_pcts = {}
    csv = open(filename)
    lines = []
    for line in csv:
        lines.append(line.strip())
    archetypes_col = lines[0].split(',')[1:]
    archetypes = []
    for line in lines[1:]:
        tmp = line.split(',')
        i = tmp[0]
        archetypes.append(i)
        for (j, pct) in zip(archetypes_col,tmp[1:]):
            win_pcts[(i,j)] = float(pct) / float(scaling)
    return win_pcts, archetypes

if __name__ == "__main__":
    win_pcts, num_games, game_count, archetypes, overall_wr = get_win_pcts(min_game_threshold=200, min_game_count=100, limitTop=40)
    print(wr_from_csv('wr.csv'))
