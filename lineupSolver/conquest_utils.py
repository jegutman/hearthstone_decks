# some assumptions on formating
# whatever deck a player is forced to play should be listed first (for 3v2 and 2v2 scenarios, irrelevant otherwise)

# branching calcs
# 16 x ban phase
# assume order doesn't matter
# branch on both possible results

def get_win_pct(a,b, win_pcts):
    if win_pcts == 'test':
        #return 0.6
        if b == 4:
            value = 0.8
            print a,b, value
            return value
        else:
            value = 0.4
            print a,b, value
            return value
    return win_pcts[(a,b)]

def pre_ban_old(decks_a, decks_b, win_pcts):
    ban_grid = {}
    for i in range(0, len(decks_a)):
        for j in range(0, len(decks_b)):
            ban_grid[(decks_b[j],decks_a[i])] = post_ban(decks_a[:i] + decks_a[i+1:], decks_b[:j] + decks_b[j+1:], win_pcts)
    return ban_grid

def win_rate(decks_a, decks_b, win_pcts):
    res = pre_ban(decks_a, decks_b, win_pcts)
    return max(res.values())

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
            res = post_ban(tmp_a,tmp_b, win_pcts)
            #mins[d2].append(res)
            mins[d2] = min(mins[d2], res)
    return mins

def post_ban(decks_a, decks_b, win_pcts):
    if len(decks_b) == 0 and len(decks_a) > 0:
        return 0
    elif len(decks_a) == 0 and len(decks_b) > 0:
        return 1
    else:
        res = 0
        pct = get_win_pct(decks_a[0], decks_b[0], win_pcts)
        res += pct * post_ban(decks_a[1:], decks_b[:], win_pcts)
        res += (1-pct) * post_ban(decks_a[:], decks_b[1:], win_pcts)
        return res
