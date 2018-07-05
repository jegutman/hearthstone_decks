from shared_utils import *
import itertools

def win_rate(decks_a, decks_b, win_pcts):
    res = pre_ban(decks_a, decks_b, win_pcts)
    return max(res.items(), key=lambda x:x[1])


def ban_3(decks_a, decks_b, pool_a, pool_b):
    pass

def eval_final(decks_a, decks_b, win_pcts):
    total = 0.0
    count = 0
    for i in decks_a:
        for j in decks_b:
            #if get_win_pct(i, j, win_pcts) != 1- get_win_pct(j, i, win_pcts):
            #    print(i, j,get_win_pct(i, j, win_pcts))
            total += get_win_pct(i, j, win_pcts)
            count += 1
    return total / count
