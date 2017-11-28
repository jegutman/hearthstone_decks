from parseWinRates import win_pcts as vs_win_pcts, archetypes as vs_a
from json_win_rates import *

hs_win_pcts, num_games, game_count, archetypes = get_win_pcts(200)

examples = []
for i in vs_a:
  for j in vs_a:
    hs_i = vs_arch_map[i]
    hs_j = vs_arch_map[j]
    wr1 = round(vs_win_pcts[(i,j)], 3)
    wr2 = round(hs_win_pcts[(hs_i, hs_j)], 3)
    if hs_i == 'Jade Druid' and hs_j == 'Big Priest':
        print hs_i, hs_j, wr2
    if abs(wr1 - wr2) > 0.10:
      examples.append([i, j, wr1, wr2, num_games[(hs_i, hs_j)], round(wr1-wr2, 3)])


print "%-18s %-18s %6s %6s %6s" % ("deck1", "deck2", "vs%", "hs%", "diff")
for i, j, wr1, wr2, num_games, diff in sorted(examples, key=lambda x:abs(x[-1]), reverse=True):
  print "%-18s %-18s %6s %6s %6s %6s" % (i, j, wr1, wr2, num_games, diff)

