from shared_utils import *
import itertools
# some assumptions on formating
# whatever deck a player is forced to play should be listed first (for 3v2 and 2v2 scenarios, irrelevant otherwise)

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

def pre_ban(decks_a, decks_b, win_pcts):
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
            mins[d2] = round(min(mins[d2], res), 3)
    return mins

tested = {}

def avg(x):
    return sum(x) / float(len(x))

def post_ban(decks_a, decks_b, win_pcts, useGlobal=True, start=True):
    if start:
        #combos_a = list(itertools.permutations(range(0,len(decks_a))))
        combos_a = list(itertools.permutations(range(1,len(decks_a))))
        combos_b = list(itertools.permutations(range(0,len(decks_b))))
        res = []
        for x in combos_a:
            for y in combos_b:
                tmp_a = [decks_a[0]] + [decks_a[i] for i in x]
                tmp_b = [decks_b[j] for j in y]
                res.append(post_ban(tmp_a, tmp_b, win_pcts, useGlobal=useGlobal, start=False))
        return avg(res)
    if useGlobal:
        global tested
        tuple_a = tuple(sorted(decks_a))
        tuple_b = tuple(sorted(decks_b))
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
