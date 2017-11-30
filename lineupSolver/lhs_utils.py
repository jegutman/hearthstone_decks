from shared_utils import *
# some assumptions on formating
# whatever deck a player is forced to play should be listed first (for 3v2 and 2v2 scenarios, irrelevant otherwise)

# branching calcs
# 16 x ban phase
# assume order doesn't matter
# branch on both possible results

def win_rate(decks_a, decks_b, win_pcts,useGlobal=True):
    res = pre_ban(decks_a, decks_b, win_pcts,useGlobal=useGlobal)
    return max(res.items(), key=lambda x:x[1])

def pre_ban(decks_a, decks_b, win_pcts,useGlobal=True):
    mins = {}
    for d2 in decks_b:
        #mins[d2] = []
        mins[d2] = 1
        for d1 in decks_a:
            tmp_a = decks_a[:]
            tmp_b = decks_b[:]
            tmp_a.remove(d1)
            tmp_b.remove(d2)
            res = pre_pick_average(tmp_a,tmp_b, win_pcts, useGlobal=useGlobal)
            #mins[d2].append(res)
            mins[d2] = round(min(mins[d2], res), 4)
    return mins

def pre_matrix(decks_a, decks_b, win_pcts,useGlobal=True):
    cross = {}
    for d2 in decks_b:
        for d1 in decks_a:
            tmp_a = decks_a[:]
            tmp_b = decks_b[:]
            tmp_a.remove(d1)
            tmp_b.remove(d2)
            res = pre_pick_average(tmp_a,tmp_b, win_pcts, useGlobal=useGlobal)
            cross[(d2, d1)] = round(res, 4)
    return cross

def pre_pick_average(decks_a, decks_b, win_pcts, useGlobal=True):
    all_res = []
    for i in decks_a:
        for j in decks_b:
            res = post_pick(decks_a,
                            decks_b,
                            win_pcts, i, j,
                            useGlobal=useGlobal)
            all_res.append(res)
    return sum(all_res) / len(all_res)

tested = {}
def post_pick(decks_a, decks_b, win_pcts, a_pick=None, b_pick=None, useGlobal=True):
    if useGlobal:
        global tested
        tuple_a = tuple(decks_a)
        tuple_b = tuple(decks_b)
        if (tuple_a, tuple_b, a_pick, b_pick) in tested:
            return tested[(tuple_a, tuple_b, a_pick, b_pick)]
    if len(decks_b) == 0 and len(decks_a) > 0:
        return 0
    elif len(decks_a) == 0 and len(decks_b) > 0:
        return 1
    elif len(decks_a) == 1:
        res = 1
        i = decks_a[0]
        for j in decks_b:
            res *= get_win_pct(i, j, win_pcts)
        return res
    elif len(decks_b) == 1:
        tmp_res = 1
        j = decks_b[0]
        for i in decks_a:
            tmp_res *= get_win_pct(j, i, win_pcts)
        return 1 - tmp_res
    else:
        if a_pick is None:
            a_pick = decks_a[0]
        if b_pick is None:
            b_pick = decks_b[0]
        pct = get_win_pct(a_pick, b_pick, win_pcts)
        res = 0
        # win case
        tmp_b = [d for d in decks_b if d != b_pick]
        res += pct * min([post_pick(decks_a, tmp_b, win_pcts, a_pick=a_pick, b_pick=j) for j in tmp_b])
        # loss case
        tmp_a = [d for d in decks_a if d != a_pick]
        res += (1-pct) * max([post_pick(tmp_a, decks_b, win_pcts, a_pick=i, b_pick=b_pick) for i in tmp_a])
        if useGlobal:
            tested[(tuple_a, tuple_b, a_pick, b_pick)] = res
        return res
