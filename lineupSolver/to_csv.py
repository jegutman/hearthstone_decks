import sys
from json_win_rates import *


output_file = sys.argv[1]

win_pcts, num_games, game_count, archetypes, overall_wr = get_win_pcts(min_game_threshold=200, min_game_count=100, limitTop=40)
output = open(output_file, 'w')
archetypes = sorted(archetypes, key=lambda x:game_count.get(x, 0), reverse=True)
res = wr_to_csv(win_pcts, archetypes, 100)
for line in res:
    output.write(line)
output.close()
