from shared_utils import *
from json_win_rates import *
from conquest_utils import *

def target(lineups_to_test, weights = None, archetypes = None, lineups = None, archetype_map = None):
    res = ""
    win_pcts, num_games, game_count, archetypes_tmp, overall_wr = get_win_pcts(min_game_threshold=0, min_game_count=0, limitTop=30)
    if not archetypes:
        archetypes = archetypes_tmp
    if not weights:
        weights = [1 for i in lineups_to_test]
    if lineups == None or achetype_map == None:
        lineups, archetype_map = generate_lineups(archetypes)
    #print "TESTING vs LINEUPS"
    #for l in lineups_to_test:
    #    print "%-80s" % ("   ".join(l)), '"' + ",".join(l) + '"'
    #print "\n"

    win_rates_against_good = {}

    for lineup in lineups:
        lineup = get_lineup(lineup, archetype_map)
        for lu_test in lineups_to_test:
            win_rates_against_good[lineup] = win_rates_against_good.get(lineup, []) + [win_rate(list(lineup), lu_test, win_pcts)]

    #for i,j in sorted(win_rates_against_good.items())[:3]:
    #    print i,j

    lu_strings = []
    #for i,j in sorted(win_rates_against_good.items(), key=lambda x:sum([i[1] for i in x[1]]))[-10:]:
    #for i,j in sorted(win_rates_against_good.items(), key=lambda x:min([i[1] for i in x[1]]))[-10:]:
    #for i,j in sorted(win_rates_against_good.items(), key=lambda x:sumproduct_normalize([i[1] for i in x[1]],weights) * 2 + min([i[1] for i in x[1]]))[-10:]:
    for i,j in sorted(win_rates_against_good.items(), key=lambda x:sumproduct_normalize([i[1] for i in x[1]],weights)):
        #i_print = "    " + "".join(["%-20s" % x for x in i])
        #print "%-80s %s %s" % (i_print,j, round(sum([x[1] for x in j])/len(j),3)), '"' + ",".join(i) + '"'
        #print "%-80s %s %s" % (i_print,j, round(sum([x[1] for x in j])/len(j),3))
        lineup_string = ",".join(i)
        lu_strings.append((lineup_string, round(sum([x[1] for x in j])/len(j),3), round(sumproduct_normalize([i[1] for i in j],weights),3), round(min([x[1] for x in j]),3)))
        #print '         "' + lineup_string + '"'
    for i,j,k,l in lu_strings:
        res += str(" ".join([str(i) for i in ["".join(["%-20s" % x for x in i.split(',')]), j, k, l, '    "%(i)s"' % locals()]])) + '\n'
    return res


