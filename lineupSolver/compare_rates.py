import sys
sys.path.append('../')
from config import basedir
from shared_utils import *
from json_win_rates import *

#hs_win_pcts, num_games, game_count, archetypes = get_win_pcts()

date = '0118'
if len(sys.argv) == 1:
    file1 = 'win_rates/hsreplay%(date)slegend.json' % locals()
    #file1 = 'win_rates/hsreplay%(date)s.json' % locals()
    #date = '0118'
    file2 = 'win_rates/hsreplay%(date)s.json' % locals()
else:
    file1 = sys.argv[1]
    file2 = sys.argv[2]

win_pcts_1, num_games_1, game_count_1, hsreplay_archetypes_1, overall_wr_1 = get_win_pcts(min_game_threshold=0, min_game_count=0, min_win_pct=0, filename=file1,limitTop=40)
win_pcts_2, num_games_2, game_count_2, hsreplay_archetypes_2, overall_wr_2 = get_win_pcts(min_game_threshold=0, min_game_count=0, min_win_pct=0, filename=file2,limitTop=40)

top_archetypes_1 = sorted(game_count_1.keys(),key=lambda x:game_count_1.get(x,0), reverse=True)[:8]
top_archetypes_2 = sorted(game_count_2.keys(),key=lambda x:game_count_2.get(x,0), reverse=True)[:12]

res = []
for i in range(0, len(top_archetypes_1)):
    for j in range(i+1, len(top_archetypes_1)):
        a, b = top_archetypes_1[i], top_archetypes_1[j]
        wr1 = round(win_pcts_1.get((a,b),0) * 100, 1)
        wr2 = round(win_pcts_2.get((a,b),0) * 100, 1)
        diff = wr1 - wr2
        ng1 = num_games_1[(a,b)]
        ng2 = num_games_2[(a,b)]
        res.append((a,b, wr1, wr2, diff, ng1, ng2))
        #print("%-25s %-25s %s %s %5s %7s %7s" % (a,b, wr1, wr2, diff, ng1, ng2))

for i in sorted(res, key=lambda x:x[4]):
    a,b, wr1, wr2, diff, ng1, ng2 = i
    print("%-25s %-25s %s %s %5s %7s %7s" % (a,b, wr1, wr2, diff, ng1, ng2))
    


#def get_win_pcts(min_game_threshold=0, min_game_count=0, min_win_pct=0):
#    return win_pcts, num_games, game_count, hsreplay_archetypes, overall_wr
