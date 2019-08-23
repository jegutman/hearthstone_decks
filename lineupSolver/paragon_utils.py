from shared_utils import *
import nashpy
import random

pick_res = {}
def pick_phase(decks_a, decks_b, win_pcts, useGlobal=True, win_rem=1):
    if len(decks_a) == win_rem:
        return (1.0, [], [])
    if len(decks_b) == win_rem:
        return (0.0, [], [])
    #key = (tuple(sorted(decks_a, key=deckfoo)), tuple(sorted(decks_b, key=deckfoo)))
    key = (tuple(sorted(decks_a)), tuple(sorted(decks_b)))
    if key in pick_res:
        return pick_res[key]
    pairs = {}
    matrix = []
    opp_matrix = []
    for d1 in decks_a:
        tmp = []
        for d2 in decks_b:
            tmp_a = [d for d in decks_a if d != d1]
            tmp_b = [d for d in decks_b if d != d2]
            wr = get_win_pct(d1, d2, win_pcts, allow_none=False)
            res = wr * pick_phase(tmp_a, decks_b, win_pcts, useGlobal=useGlobal, win_rem=win_rem)[0] + (1 - wr) * pick_phase(decks_a, tmp_b, win_pcts, useGlobal=useGlobal, win_rem=win_rem)[0]
            pairs[(d1, d2)] = res
            tmp.append(res)
        matrix.append(tmp)
        opp_matrix.append([1-x for x in tmp])
    ng = nashpy.game.Game(matrix,opp_matrix)
    tmp = list(ng.support_enumeration(non_degenerate=True))
    #print(decks_a, decks_b)
    #print('x', tmp)
    e, f = tmp[0]
    h = [_x for _x in zip(e,decks_b)]
    g = [_x for _x in zip(f,decks_a)]
    #pick_res[key] = (ng[e,f][0], matrix, g, h)
    pick_res[key] = (ng[e,f][0], pairs, g, h)
    return pick_res[key]
    #return ng[e,f], matrix, g, h

ban_res = {}
def ban_phase(decks_a, decks_b, win_pcts, useGlobal=True, win_rem=1):
    #key = (tuple(decks_a[:1] + sorted(decks_a[1:], key=deckfoo)), tuple(decks_b[:1] + sorted(decks_b[1:], key=deckfoo)))
    key = (tuple(decks_a[:1] + sorted(decks_a[1:])), tuple(decks_b[:1] + sorted(decks_b[1:])))
    if key in ban_res:
        return ban_res[key]
    pairs = {}
    matrix = []
    opp_matrix = []
    pairs = {}
    for d2 in decks_b[1:]:
        tmp = []
        for d1 in decks_a[1:]:
            tmp_a = [d for d in decks_a if d != d1]
            tmp_b = [d for d in decks_b if d != d2]
            res = pick_phase(tmp_a, tmp_b, win_pcts, useGlobal=useGlobal, win_rem=win_rem)[0]
            pairs[(d2, d1)] = res
            tmp.append(res)
        matrix.append(tmp)
        opp_matrix.append([1-x for x in tmp])
    ng = nashpy.game.Game(matrix,opp_matrix)
    e,f = list(ng.support_enumeration(non_degenerate=True))[0]
    h = [_x for _x in zip(e,decks_a[1:])]
    g = [_x for _x in zip(f,decks_b[1:])]
    #ban_res[key] = (ng[e,f][0], matrix, g, h)
    ban_res[key] = (ng[e,f][0], pairs, g, h)
    return ban_res[key]
    #return ng[e,f], matrix, g, h

protect_res = {}
def protect_phase(decks_a, decks_b, win_pcts, useGlobal=True, win_rem=1):
    #key = (tuple(sorted(decks_a, key=deckfoo)), tuple(sorted(decks_b, key=deckfoo)))
    key = (tuple(sorted(decks_a)), tuple(sorted(decks_b)))
    #if key in protect_res:
    #    return protect_res[key]
    pairs = {}
    matrix = []
    opp_matrix = []
    for d1 in decks_a:
        tmp = []
        for d2 in decks_b:
            tmp_a = [d1] + [d for d in decks_a if d != d1]
            tmp_b = [d2] + [d for d in decks_b if d != d2]
            res = ban_phase(tmp_a, tmp_b, win_pcts, useGlobal=useGlobal, win_rem=win_rem)[0]
            pairs[(d2, d1)] = res
            tmp.append(res)
        matrix.append(tmp)
        opp_matrix.append([1-x for x in tmp])
    ng = nashpy.game.Game(matrix,opp_matrix)
    e,f = list(ng.support_enumeration(non_degenerate=True))[0]
    #h = sorted([_x for _x in zip(f,decks_b)], key=deckfoo2)
    h = sorted([_x for _x in zip(f,decks_b)])
    #g = sorted([_x for _x in zip(e,decks_a)], key=deckfoo2)
    g = sorted([_x for _x in zip(e,decks_a)])
    #protect_res[key] = (ng[e,f][0], matrix, g, h)
    protect_res[key] = (ng[e,f][0], pairs, g, h)
    return protect_res[key]

def deckfoo(deck):
    return (deck.split(' ')[-1], deck)

def deckfoo2(deck):
    value, deck = deck
    return (deck.split(' ')[-1], deck)

if __name__ == '__main__':
    import sys
    sys.path.append('../')
    from config import basedir
    sys.path.append(basedir)
    sys.path.append(basedir + '/lineupSolver')

    from shared_utils import *
    from json_win_rates import * 
    win_pcts, num_games, game_count, archetypes, overall_wr = get_win_pcts(min_game_threshold=0, min_game_count=0,limitTop=100)
    
    #lu = ['Mill Druid', 'Odd Paladin', 'Clone Priest', 'Odd Rogue']
    #lu = ['Odd Paladin', 'Shudderwock Shaman', 'Odd Rogue', 'Malygos Druid']
    lu = ['Combo Priest', 'Control Warrior', 'Tempo Rogue', 'Highlander Mage' ]
    lu2 = ['Quest Shaman', 'Aggro Warrior', 'Murloc Paladin', 'Secret Hunter']
    pb = lu[1:]
    pb2 = lu2[1:]
    win_rates_grid(lu, lu2, win_pcts)
    random.shuffle(lu)
    random.shuffle(lu2)
    print(str(lu) + "\n" + str(lu2))
    print(lu, lu2)
    tmp = protect_phase(lu, lu2, win_pcts)
    print(tmp)
    a, b = max(tmp[1])[1], max(tmp[2])[1]
    print(str(lu) + "\n" + str(lu2))
    lu = [a] + [l for l in lu if l!=a]
    lu2 = [b] + [l for l in lu2 if l!=b]
    print(a + "\n" + b)
    print(str(lu) + "\n" + str(lu2))
    
    #print("")
    #print(ban_phase(lu, lu2, win_pcts))
    #for i in range(0, 100):
    #    random.shuffle(pb)
    #    random.shuffle(pb2)
    #    lu = lu[:1] + pb
    #    lu2 = lu2[:1] + pb2
    #    print(protect_phase(lu, lu2, win_pcts))
    #print(pick_phase(lu, lu2, win_pcts))
