from shared_utils import *
from json_win_rates import * 
from conquest_utils import win_rates_lines as cq_win_rates_lines
from conquest_utils import post_ban as cq_post_ban
from conquest_utils import win_rate as cq_win_rate
from conquest_utils import pre_ban as cq_pre_ban
from conquest_utils import pre_ban_old as cq_pre_ban_old
from lhs_utils import win_rates_lines as lhs_win_rates_lines
from lhs_utils import win_rate as lhs_win_rate
from lhs_utils import pre_ban as lhs_pre_ban
from lhs_utils import pre_matrix
from lhs_utils import lead_matrix

win_pcts, num_games, game_count, archetypes, overall_wr = get_win_pcts(min_game_threshold=0, min_game_count=0)
overrides = [
            ]
win_pcts = override_wr(overrides,win_pcts)

def sim(my_lineup, opp_lineup):
    res = ""
    #assert all([d in archetypes for d in my_lineup]), ([d in archetypes for d in my_lineup], my_lineup)
    for d in my_lineup:
        if d not in archetypes:
            return 'Could not recognize archetype: "%s"' % d
    for d in opp_lineup:
        if d not in archetypes:
            return 'Could not recognize archetype: "%s"' % d
    #assert all([d in archetypes for d in opp_lineup]), ([d in archetypes for d in opp_lineup], opp_lineup)

    res += str(my_lineup) +  " vs " + str(opp_lineup) + '\n'
    res += cq_win_rates_lines(my_lineup, opp_lineup, win_pcts,num_games) + '\n'
    res += str(cq_win_rate(my_lineup, opp_lineup, win_pcts)) + '\n'
    res += str(cq_pre_ban(my_lineup, opp_lineup, win_pcts)) + '\n'

    #res_ban = cq_pre_ban_old(my_lineup,
    #                         opp_lineup,
    #                         win_pcts)
    return res

def cq_bans(my_lineup, opp_lineup):
    res = ""
    for d in my_lineup:
        if d not in archetypes:
            return 'Could not recognize archetype: "%s"' % d
    for d in opp_lineup:
        if d not in archetypes:
            return 'Could not recognize archetype: "%s"' % d
    res += "bans" + '\n'
    res += "%-20s %-20s" % ("p1_ban", "p2_ban") + '\n'
    #for i, j in sorted(res.items(), key=lambda x:-x[1]):
    res_ban = cq_pre_ban_old(my_lineup,
                             opp_lineup,
                             win_pcts)
    for i, j in sorted(res_ban.items(), key=lambda x:(x[0][0], x[1])):
        d1, d2 = i
        res += '%-20s %-20s %s' % (d1, d2, round(j,4)) + '\n'
    return res

def lhs_bans(my_lineup, opp_lineup):
    res = ""
    res_ban = pre_matrix(my_lineup,
                      opp_lineup,
                      win_pcts)
    res += "bans" + '\n'
    res += "%-20s %-20s" % ("p1_ban", "p2_ban") + '\n'
    for i, j in sorted(res_ban.items(), key=lambda x:(x[0][0], x[1])):
        d1, d2 = i
        res += '%-20s %-20s %s' % (d1, d2, round(j,4)) + '\n'
    return res

def lhs_leads(my_lineup, opp_lineup):
    res = ""
    res_lead = lead_matrix(my_lineup,
                      opp_lineup,
                      win_pcts)
    res += "leads" + '\n'
    res += "%-20s %-20s" % ("p1_lead", "p2_lead") + '\n'
    totals = {}
    counts = {}
    for i, j in sorted(res_lead.items(), key=lambda x:(x[0][1], -x[1])):
        d1, d2 = i
        totals[d1] = totals.get(d1, 0) + j
        counts[d1] = counts.get(d1, 0) + 1
        res += '%-20s %-20s %s' % (d1, d2, round(j,4)) + '\n'
    res += '\n' + 'averages:' + '\n'
    for d in sorted(totals, key=lambda x:totals[x], reverse=True):
        res += '%-20s : %s'  % (d, round(totals[d] / counts[d], 4)) + '\n'
    #print(my_lineup, opp_lineup, res)
    return res

def sim_lhs(my_lineup, opp_lineup):
    res = ""
    assert all([d in archetypes for d in my_lineup]), ([d in archetypes for d in my_lineup], my_lineup)
    assert all([d in archetypes for d in opp_lineup]), ([d in archetypes for d in opp_lineup], opp_lineup)

    res +=  str(my_lineup) +  " vs " + str(opp_lineup) + '\n'
    res += lhs_win_rates_lines(my_lineup, opp_lineup, win_pcts,num_games) + '\n'
    res += str(lhs_win_rate(my_lineup, opp_lineup, win_pcts)) + '\n'
    res += str(lhs_pre_ban(my_lineup, opp_lineup, win_pcts)) + '\n'

    #res_ban = lhs_pre_ban_old(my_lineup,
    #                          opp_lineup,
    #                          win_pcts)
    return res
