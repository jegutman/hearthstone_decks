from shared_utils import *
import itertools
# some assumptions on formating
# whatever deck a player is forced to play should be listed first (for 3v2 and 2v2 scenarios, irrelevant otherwise)
import random
import nashpy

# branching calcs
# 16 x ban phase
# assume order doesn't matter
# branch on both possible results

def pre_ban_old(decks_a, decks_b, win_pcts):
    ban_grid = {}
    for i in range(0, len(decks_a)):
        for j in range(0, len(decks_b)):
            ban_grid[(decks_b[j],decks_a[i])] = post_ban(decks_a[:i] + decks_a[i+1:], decks_b[:j] + decks_b[j+1:], win_pcts)
    return ban_grid

def win_rate(decks_a, decks_b, win_pcts):
    res = pre_ban(decks_a, decks_b, win_pcts)
    return max(res.items(), key=lambda x:x[1])

def win_rate_nash_calc(decks_a, decks_b, win_pcts):
    res = pre_ban_matrix(decks_a, decks_b, win_pcts)
    opp_res = []
    for i in res:
        opp_res.append([1-j for j in i])
    ng = nashpy.game.Game(res,opp_res)
    e,f = list(ng.lemke_howson_enumeration())[0]
    return ng[e,f][0]

def win_rate_nash(decks_a, decks_b, win_pcts):
    res = pre_ban_matrix(decks_a, decks_b, win_pcts)
    opp_res = []
    for i in res:
        opp_res.append([1-j for j in i])
    ng = nashpy.game.Game(res,opp_res)
    e,f = list(ng.lemke_howson_enumeration())[0]
    g = zip(e,decks_b)
    h = zip(f,decks_a)
    return ng[e,f], g,h 

def calculate_win_rate(decks_a, decks_b, win_pcts):
    res = pre_ban(decks_a, decks_b, win_pcts)
    return max(res.items(), key=lambda x:x[1])[1]

def pre_ban(decks_a, decks_b, win_pcts, debug=False):
    mins = {}
    for d2 in decks_b:
        #mins[d2] = []
        mins[d2] = 1
        for d1 in decks_a:
            tmp_a = decks_a[:]
            tmp_b = decks_b[:]
            tmp_a.remove(d1)
            tmp_b.remove(d2)
            res = post_ban(tmp_a, tmp_b, win_pcts)
            #mins[d2].append(res)
            mins[d2] = round(min(mins[d2], res), 4)
    return mins

def pre_ban_matrix(decks_a, decks_b, win_pcts, debug=False):
    res_matrix = []
    for d2 in decks_b:
        tmp = []
        for d1 in decks_a:
            tmp_a = decks_a[:]
            tmp_b = decks_b[:]
            tmp_a.remove(d1)
            tmp_b.remove(d2)
            tmp.append(post_ban(tmp_a, tmp_b, win_pcts))
            #mins[d2] = round(min(mins[d2], res), 4)
        res_matrix.append(tmp)
    return res_matrix

tested = {}

def avg(x):
    return sum(x) / float(len(x))

def post_ban(decks_a, decks_b, win_pcts, useGlobal=True, start=True, return_list=False):
    if useGlobal:
        global tested
        tuple_a = tuple(list(decks_a) + ['start'])
        tuple_b = tuple(list(decks_b) + ['start'])
        if (tuple_a, tuple_b) in tested:
            return tested[(tuple_a, tuple_b)]
    if start:
        combos_a = list(itertools.permutations(decks_a))
        combos_b = list(itertools.permutations(decks_b))
        res = []
        for x in combos_a:
            for y in combos_b:
                res.append(post_ban(x, y, win_pcts, useGlobal=useGlobal, start=False))
            #res.append(post_ban(x, decks_b, win_pcts, useGlobal=useGlobal, start=False))
        if not return_list:
            if useGlobal:
                tested[(tuple_a, tuple_b)] = avg(res)
            return avg(res)
        else:
            return avg(res), res
    if useGlobal:
        tuple_a = tuple(decks_a)
        tuple_b = tuple(decks_b)
        if (tuple_a, tuple_b) in tested:
            return tested[(tuple_a, tuple_b)]
    if len(decks_b) == 0 and len(decks_a) > 0:
        return 0
    elif len(decks_a) == 0 and len(decks_b) > 0:
        return 1
    else:
        res = 0
        pct = get_win_pct(decks_a[0], decks_b[0], win_pcts)
        res += pct * post_ban(decks_a[1:], decks_b[:], win_pcts, useGlobal=useGlobal, start=False)
        res += (1-pct) * post_ban(decks_a[:], decks_b[1:], win_pcts, useGlobal=useGlobal, start=False)
        if useGlobal:
            tested[(tuple_a, tuple_b)] = res
        return res

def post_ban_single(decks_a, decks_b, win_pcts):
    possible_wins = list(itertools.permutations(range(0, len(deck_a) + len(decks_b) - 1)))
    for i in range(0, possible_wins):
        tmp = possible_wins[i]
        while tmp[-1] == 0:
            tmp = tmp[:-1]
    #if start==False:
    #    assert False, (decks_a, decks_b)
    if start:
        #combos_a = list(itertools.permutations(range(0,len(decks_a))))
        combos_a = list(itertools.permutations(range(0,len(decks_a))))
        combos_b = list(itertools.permutations(range(0,len(decks_b))))
        res = []
        for x in combos_a:
            for y in combos_b:
                #tmp_a = [decks_a[0]] + [decks_a[i] for i in x]
                tmp_a = [decks_a[i] for i in x]
                tmp_b = [decks_b[j] for j in y]
                res.append(post_ban(tmp_a, tmp_b, win_pcts, useGlobal=useGlobal, start=False))
        if not return_list:
            return avg(res)
        else:
            return avg(res), res
    if len(decks_b) == 0 and len(decks_a) > 0:
        return 0
    elif len(decks_a) == 0 and len(decks_b) > 0:
        return 1
    else:
        res = 0
        pct = get_win_pct(decks_a[0], decks_b[0], win_pcts)
        res += pct * post_ban(decks_a[1:], decks_b[:], win_pcts, useGlobal=useGlobal, start=False)
        res += (1-pct) * post_ban(decks_a[:], decks_b[1:], win_pcts, useGlobal=useGlobal, start=False)
        if useGlobal:
            tested[(tuple_a, tuple_b)] = res
        return res

def intra_match(decks_a, decks_b, win_pcts):
    #if start==False:
    #    assert False, (decks_a, decks_b)
    res = 0
    pct = get_win_pct(decks_a[0], decks_b[0], win_pcts)
    res += pct * post_ban(decks_a[1:], decks_b[:], win_pcts, useGlobal=False, start=True)
    res += (1-pct) * post_ban(decks_a[:], decks_b[1:], win_pcts, useGlobal=False, start=True)
    return res


def group_scores(scores):
    groups = []
    group = []
    lastScore = 99999
    randomize = {}
    for player in scores:
        randomize[player] = random.random()
        
    for player, score in sorted(scores.items(), key=lambda x:(x[1], randomize[x[0]]), reverse=True):
        if score != lastScore:
            lastScore = score
            if group:
                groups.append(group)
                group = []
        group.append((player, score))
    groups.append(group)
    for i in range(0, len(groups)-1):
        if len(groups[i]) % 2 == 1:
            groups[i] = groups[i] + groups[i+1][:1]
            groups[i+1] = groups[i+1][1:]
    return groups

def simulate_matchup(p1, p2, l1, l2, win_pcts):
    pct = calculate_win_rate(l1, l2, win_pcts)
    if random.random() < pct:
        return 1
    return 0

def get_sim_matchup(decks, win_pcts, rating=""):
    lineups = list([tuple(i) for i in decks.values()])
    players = list(decks.keys())
    mu_pcts = {}
    for i in range(0, len(lineups)):
        for j in range(i, len(lineups)):
            l1 = tuple(lineups[i])
            l2 = tuple(lineups[j])
            p1 = players[i]
            p2 = players[j]
            sim_res = calculate_win_rate(list(l1), list(l2), win_pcts)
            #mu_pcts[(l1, l2)] = sim_res
            #mu_pcts[(l2, l1)] = 1 - sim_res
            mu_pcts[(p1, p2)] = sim_res
            mu_pcts[(p2, p1)] = 1 - sim_res

    def sim_matchup(p1, p2, l1, l2, win_pcts):
        #pct = mu_pcts[(tuple(l1), tuple(l2))]
        pct = mu_pcts[(p1, p2)]
        if random.random() < pct:
            return 1
        return 0
    return sim_matchup, mu_pcts

def expect_score_local(r1, r2):
    rating_diff = r2 - r1
    return 1 / (1 + 10 ** (rating_diff / 1135.77))

def get_sim_matchup_rating(decks, win_pcts, rating):
    #lineups = list(set([tuple(i) for i in decks.values()]))
    lineups = list([tuple([i] +  j) for i,j in decks.items()])
    mu_pcts = {}
    for i in range(0, len(lineups)):
        for j in range(i, len(lineups)):
            ind1 = tuple(lineups[i])
            ind2 = tuple(lineups[j])
            l1 = tuple(lineups[i][1:])
            l2 = tuple(lineups[j][1:])
            p1 = lineups[i][0]
            p2 = lineups[j][0]
            sim_res = calculate_win_rate(list(l1), list(l2), win_pcts)
            r1 = rating[p1.lower()]
            r2 = rating[p2.lower()]
            elo_adjust = r1.env.calc_diff(sim_res)
            sim_res_blended = round(expect_score_local(r1.mu + elo_adjust, r2.mu),4)
            mu_pcts[(ind1, ind2)] = sim_res_blended
            mu_pcts[(ind2, ind1)] = 1 - sim_res_blended

    def sim_matchup(p1, p2, l1, l2, win_pcts):
        ind1 = tuple([p1] + l1)
        ind2 = tuple([p2] + l2)
        pct = mu_pcts[(tuple(ind1), tuple(ind2))]
        if random.random() < pct:
            return 1
        return 0
    return sim_matchup, mu_pcts

def simulate_round(decks, scores, win_pcts, simulate_matchup=simulate_matchup):
    groups = group_scores(scores)
    for group in groups:
        if len(group) % 2 == 1:
            scores[group[-1][0]] += 1
            group = group[:-1]
        group_size = len(group)
        for i in range(0, int(group_size / 2)):
            p1 = group[i][0]
            p2 = group[i + int(group_size / 2)][0]
            match = simulate_matchup(p1, p2, decks[p1], decks[p2], win_pcts)
            scores[p1] += match
            scores[p2] += (1 - match)

def simulate_round_ko(decks, scores, win_pcts, simulate_matchup=simulate_matchup):
    groups = group_scores(scores)
    for group in groups:
        group_size = len(group)
        for i in range(0, group_size, 2):
            p1 = group[i][0]
            p2 = group[i + 1][0]
            match = simulate_matchup(p1, p2, decks[p1], decks[p2], win_pcts)
            scores[p1] += match
            scores[p2] += (1 - match)
    to_remove = []
    for i in scores.keys():
        if scores[i] == 0:
            to_remove.append(i)
    for i in to_remove:
        scores.pop(i)

def simulate_group(decks, group, win_pcts, simuate_matchup=simulate_matchup):
    
    # odds player wins group =
    # % win first game * ( % win one of 2nd game or 3rd game)
    # + % lose first game * % win 2nd game and 3rd game
    pass

def simulate_tournament(decks, rounds, scores=None, win_pcts={},simulate_matchup=simulate_matchup):
    if scores == None:
        scores = {}
        for d in decks.keys():
            scores[d] = 0
    for i in range(0, rounds):
        simulate_round(decks, scores, win_pcts, simulate_matchup=simulate_matchup)
    return scores

def simulate_tournament_ko(decks, rounds, scores=None, win_pcts={},simulate_matchup=simulate_matchup):
    if scores == None:
        scores = {}
        for d in decks.keys():
            scores[d] = 0
    for i in range(0, rounds):
        simulate_round_ko(decks, scores, win_pcts, simulate_matchup=simulate_matchup)
    return scores
