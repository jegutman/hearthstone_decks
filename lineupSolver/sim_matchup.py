from shared_utils import *
from json_win_rates import * 
tested = {}
from conquest_utils import tested
from conquest_utils import win_rates_lines as cq_win_rates_lines
from conquest_utils import post_ban as cq_post_ban
from conquest_utils import win_rate as cq_win_rate
from conquest_utils import pre_ban as cq_pre_ban
from conquest_utils import pre_ban_matrix as cq_pre_ban_matrix
from conquest_utils import pre_ban_old as cq_pre_ban_old
from lhs_utils import win_rates_lines as lhs_win_rates_lines
from lhs_utils import win_rate as lhs_win_rate
from lhs_utils import pre_ban as lhs_pre_ban
from lhs_utils import pre_matrix
from lhs_utils import lead_matrix
from lhs_utils import pre_pick_nash_calc
import nashpy

win_pcts, num_games, game_count, archetypes, overall_wr = get_win_pcts(min_game_threshold=0, min_game_count=0)
overrides = [
            ]
win_pcts = override_wr(overrides,win_pcts)
filename = basedir + '/lineupSolver/' + 'custom_na.csv'
win_pcts2, archetypes2 = wr_from_csv(filename, scaling=100)
win_pcts.update(win_pcts2)
archetypes = list(set(archetypes).union(set(archetypes2)))

def sim(my_lineup, opp_lineup, win_pcts=win_pcts, archetypes=archetypes):
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

def cq_bans(my_lineup, opp_lineup, win_pcts=win_pcts, archetypes=archetypes):
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

def lhs_bans(my_lineup, opp_lineup, win_pcts=win_pcts, archetypes=archetypes):
    res = ""
    res_ban = pre_matrix(my_lineup,
                      opp_lineup,
                      win_pcts,
                      archetypes)
    res += "bans" + '\n'
    res += "%-20s %-20s" % ("p1_ban", "p2_ban") + '\n'
    for i, j in sorted(res_ban.items(), key=lambda x:(x[0][0], x[1])):
        d1, d2 = i
        res += '%-20s %-20s %s' % (d1, d2, round(j,4)) + '\n'
    return res

def lhs_leads(my_lineup, opp_lineup, win_pcts=win_pcts):
    res = ""
    res_lead, matrix_lead = lead_matrix(my_lineup, opp_lineup, win_pcts)
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

def lhs_nash(decks_a, decks_b, win_pcts=win_pcts):
    for d in decks_a:
        if d not in archetypes:
            return 'Could not recognize archetype: "%s"' % d
    for d in decks_b:
        if d not in archetypes:
            return 'Could not recognize archetype: "%s"' % d
    res = ""
    res_lead, matrix_lead = lead_matrix(decks_a, decks_b, win_pcts)
    ng = nashpy.game.Game(matrix_lead)
    e,f = list(ng.support_enumeration())[0]
    g = zip(e,decks_a)
    h = zip(f,decks_b)
    win_pct = round(ng[e,f][0], 3)
    res += "leads" + '\n'
    res += "%-20s %s" % ("p1_lead", "lead_freq") + '\n'
    for i,j in sorted(g):
        res += '%-20s %s' % (j, round(i,4)) + '\n'
    res += '\n'
    res += "%-20s %s" % ("p2_lead", "lead_freq") + '\n'
    for i,j in sorted(h):
        res += '%-20s %s' % (j, round(i,4)) + '\n'
    res += '\nWin Pct p1: %s\n' % win_pct
    return res

def lhs_nash_bans(decks_a, decks_b, win_pcts=win_pcts):
    for d in decks_a:
        if d not in archetypes:
            return 'Could not recognize archetype: "%s"' % d
    for d in decks_b:
        if d not in archetypes:
            return 'Could not recognize archetype: "%s"' % d
    res = ""
    matrix = []
    opp_matrix = []
    details = []
    for d2 in decks_b:
        tmp = []
        for d1 in decks_a:
            tmp_a = decks_a[:]
            tmp_b = decks_b[:]
            tmp_a.remove(d1)
            tmp_b.remove(d2)
            tmp.append(pre_pick_nash_calc(tmp_a,tmp_b, win_pcts, useGlobal=False))
            details.append([d2,d1, round(tmp[-1], 3)])
            #details += "%-20s %-20s %s" % (d2, d1, round(tmp[-1], 3)) + '\n'
        matrix.append(tmp)
        opp_matrix.append([1-x for x in tmp])
    ng = nashpy.game.Game(matrix)
    e,f = list(ng.vertex_enumeration())[0]
    g = zip(e,decks_b)
    h = zip(f,decks_a)
    win_pct = round(ng[e,f][0], 4)
    res += "bans" + '\n'
    res += "%-20s %s" % ("p1_ban", "ban_freq") + '\n'
    for i,j in sorted(g):
        i = round(i, 2)
        if abs(i) < 0.001:
            i = 0.0
        res += '%-20s %s' % (j, round(i,2)) + '\n'
    res += '\n'
    res += "%-20s %s" % ("p2_ban", "ban_freq") + '\n'
    for i,j in sorted(h):
        i = round(i, 2)
        if abs(i) < 0.001:
            i = 0.0
        res += '%-20s %s' % (j, round(i,2)) + '\n'
    res += '\nWin Pct p1: %s\n' % win_pct
    res += "\ndetails\nbans" + '\n'
    res += "%-20s %-20s" % ("p1_ban", "p2_ban") + '\n'
    for a,b,c in sorted(details, key=lambda x:(x[0], x[2])):
        res += "%-20s %-20s %s" % (a,b,c) + '\n'
    return res

#res = pre_ban_matrix(decks_a, decks_b, win_pcts)
#opp_res = []
#for i in res:
#    opp_res.append([1-j for j in i])
#ng = nashpy.game.Game(res,opp_res)
#e,f = list(ng.lemke_howson_enumeration())[0]
#return ng[e,f][0]

def conquest_nash_bans(decks_a, decks_b, win_pcts=win_pcts, check_archetypes=True):
    if check_archetypes:
        for d in decks_a:
            if d not in archetypes:
                return 'Could not recognize archetype: "%s"' % d
        for d in decks_b:
            if d not in archetypes:
                return 'Could not recognize archetype: "%s"' % d
    res = ""
    matrix = cq_pre_ban_matrix(decks_a, decks_b, win_pcts)
    opp_matrix = cq_pre_ban_matrix(decks_b, decks_a, win_pcts)
    ng = nashpy.game.Game(matrix)
    e,f = list(ng.vertex_enumeration())[0]
    g = zip(e,decks_b)
    h = zip(f,decks_a)
    win_pct = round(ng[e,f][0], 4)
    res += "bans" + '\n'
    res += "%-20s %s" % ("p1_ban", "ban_freq") + '\n'
    for i,j in sorted(g):
        i = round(i, 2)
        if abs(i) < 0.001:
            i = 0.0
        res += '%-20s %s' % (j, round(i,2)) + '\n'
    res += '\n'
    res += "%-20s %s" % ("p2_ban", "ban_freq") + '\n'
    for i,j in sorted(h):
        i = round(i, 2)
        if abs(i) < 0.001:
            i = 0.0
        res += '%-20s %s' % (j, round(i,2)) + '\n'
    res += '\nWin Pct p1: %s\n' % win_pct
    #res += "\ndetails\nbans" + '\n'
    #res += "%-20s %-20s" % ("p1_ban", "p2_ban") + '\n'
    #for a,b,c in sorted(details, key=lambda x:(x[0], x[2])):
    #    res += "%-20s %-20s %s" % (a,b,c) + '\n'
    return res


def sim_lhs(my_lineup, opp_lineup, win_pcts=win_pcts):
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
