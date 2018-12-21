from __future__ import print_function
import sys
sys.path.append('../')
from config import basedir
sys.path.append(basedir)
sys.path.append(basedir + '/lineupSolver')
from shared_utils import *
from lhs_utils import *
import itertools
from pprint import pprint
import datetime
threshold = 0.0

class WSOE_Matchup():
    def __init__(self, l1, l2, decksA=[], decksB=[], win_pcts = None, clear_initialize=False):
        self.poolA = list(l1)
        self.poolB = list(l2)
        self.decksA = decksA
        self.decksB = decksB
        if not win_pcts:
            self.win_pcts = get_win_pcts(min_game_threshold=0, min_game_count=0,limitTop=100)[0]
        else:
            self.win_pcts = win_pcts
        #self.decksA = sorted(self.decksA, key=lambda x:sum([self.win_pcts.get((x, y), 0.5) for y in self.decksB]), reverse=True)
        #self.decksB = sorted(self.decksB, key=lambda x:sum([self.win_pcts.get((x, y), 0.5) for y in self.decksA]), reverse=True)
        if clear_initialize:
            global eval_final
            eval_final = None

    def add_ban(self, bansA=[], bansB=[]):
        for i in bansA:
            self.poolA.remove(i)
        for i in bansB:
            self.poolB.remove(i)

    def add_picks(self, picksA=[], picksB=[]):
        self.decksA += picksA
        self.decksB += picksB
        for i in picksA:
            self.poolA.remove(i)
        for i in picksB:
            self.poolB.remove(i)

    def calculate(self, isGoofy=False, useAB=True):
        poolA = self.poolA
        poolB = self.poolB
        decksA = self.decksA
        decksB = self.decksB
        if isGoofy:
            poolA, poolB = poolB, poolA
            decksA, decksB = decksB, decksA
        #assert len(poolA) == len(poolB), "pools must be equal in size"
        #assert len(decksA) == len(decksB), "decks must be equal in size"
        if len(poolB) == 9 and len(poolA) == 9:
            #ban1a
            return(ban1a(poolA, poolB, decksA, decksB, self.win_pcts, head=True, useAB=useAB))
        elif len(poolB) == 7 and len(poolA) == 9:
            #ban1b
            return(ban1b(poolA, poolB, decksA, decksB, self.win_pcts, head=True, useAB=useAB))
        elif len(poolB) == 7 and len(poolA) == 7:
            #pick1a
            return(pick1a(poolA, poolB, decksA, decksB, self.win_pcts, head=True, useAB=useAB))
        elif len(poolB) == 7 and len(poolA) == 6:
            #pick1b
            return(pick1b(poolA, poolB, decksA, decksB, self.win_pcts, head=True, useAB=useAB))
        elif len(poolB) == 6 and len(poolA) == 6:
            #ban2b
            return(ban2b(poolA, poolB, decksA, decksB, self.win_pcts, head=True, useAB=useAB))
        elif len(poolB) == 6 and len(poolA) == 4:
            #ban2a
            return(ban2a(poolA, poolB, decksA, decksB, self.win_pcts, head=True, useAB=useAB))
        elif len(poolB) == 4 and len(poolA) == 4:
            #pick2b
            return(pick2b(poolA, poolB, decksA, decksB, self.win_pcts, head=True, useAB=useAB))
        elif len(poolB) == 3 and len(poolA) == 4:
            #pick2a
            return(pick2a(poolA, poolB, decksA, decksB, self.win_pcts, head=True, useAB=useAB))
        elif len(poolB) == 3 and len(poolA) == 3:
            #ban3a
            return(ban3a(poolA, poolB, decksA, decksB, self.win_pcts, head=True, useAB=useAB))
        elif len(poolB) == 2 and len(poolA) == 3:
            #ban3b
            return(ban3b(poolA, poolB, decksA, decksB, self.win_pcts, head=True, useAB=useAB))
        elif len(poolB) == 2 and len(poolA) == 2:
            #pick3a
            return(pick3a(poolA, poolB, decksA, decksB, self.win_pcts, head=True, useAB=useAB))
        elif len(poolB) == 2 and len(poolA) == 1:
            #pick3b
            return(pick3b(poolA, poolB, decksA, decksB, self.win_pcts, head=True, useAB=useAB))
        elif len(poolB) == 1 and len(poolA) == 1:
            return eval_final_calc(decksA, decksB, self.win_pcts)
        else:
            return "Unexpected State"
            

# Ban 1a
#P1 - Ban x2 

# Ban 1b
#P2 - Ban x2 

# Pick 1a
#P1 - Pick 

# Pick 1b
#P2 - Pick 

# Ban 2b
#P2 - Ban x2 
# Ban 2a
#P1 - Ban x2 

#Pick 2b
#P2 - Pick 
#Pick 2a
#P1 - Pick 
# Ban 3a
#P1 - Ban x1 
# Ban 3b
#P2 - Ban x1 
# Pick 3a
#P1 - Pick 
# Pick 3b
#P2 - Pick 
        
        

def win_rate(decks_a, decks_b, win_pcts):
    res = pre_ban(decks_a, decks_b, win_pcts)
    return max(res.items(), key=lambda x:x[1])



def eval_final_old(decks_a, decks_b, win_pcts):
    total = 0.0
    count = 0
    for i in decks_a:
        for j in decks_b:
            total += get_win_pct(i, j, win_pcts)
            count += 1
    return total / count

def calc_bin(a,b, win_pcts, wl):
    if wl:
        return win_pcts[(a,b)]
    else:
        return 1-win_pcts[(a,b)]

wins = [
    (0, 0, 1, 1, 1),
    (0, 1, 0, 1, 1),
    (0, 1, 1, 0, 1),
    (0, 1, 1, 1, 0),
    (0, 1, 1, 1, 1),
    (1, 0, 0, 1, 1),
    (1, 0, 1, 0, 1),
    (1, 0, 1, 1, 0),
    (1, 0, 1, 1, 1),
    (1, 1, 0, 0, 1),
    (1, 1, 0, 1, 0),
    (1, 1, 0, 1, 1),
    (1, 1, 1, 0, 0),
    (1, 1, 1, 0, 1),
    (1, 1, 1, 1, 0),
    (1, 1, 1, 1, 1)
]

eval_final = None
win_rates_init = {}
def initialize(decks_a, decks_b, win_pcts, debug=False):
    global win_rates_init
    #print(decks_a, decks_b)
    res = {}
    #decks_a = sorted(decks_a, key=lambda x:x.split(' ')[-1])
    #decks_b = sorted(decks_b, key=lambda x:x.split(' ')[-1])
    decks_a = sorted(decks_a)
    decks_b = sorted(decks_b)
    all_l1 = list(itertools.combinations(decks_a, 3))
    all_l2 = list(itertools.combinations(decks_b, 3))
    print(len(all_l1), len(all_l2))
    count = 0
    #print("Initializing", len(all_l1) * len(all_l2))
    #print("len", len(list(all_l1)), len(list(all_l2)))
    for l1 in all_l1:
        for l2 in all_l2:
            #print(l1, l2)
            count += 1
            if debug:
                if count % 1000 == 0:
                    print(count)
            #res[(tuple(l1), tuple(l2))] = pre_pick_nash_calc(l1, l2, win_pcts)
            res[(tuple(l1), tuple(l2))] = pre_pick_average(l1, l2, win_pcts)
            res[(tuple(l2), tuple(l1))] = 1 - res[(tuple(l1), tuple(l2))]
    #print(res)
    win_rates_init = res
    def eval_final_tmp(decks_a, decks_b, win_pcts):
        decks_a = sorted(decks_a)
        decks_b = sorted(decks_b)
        return round(res[(tuple(decks_a), tuple(decks_b))], 6)
    global eval_final
    #print("Done Initializing")
    eval_final = eval_final_tmp
    print("DONE")

def eval_final_calc(decks_a, decks_b, win_pcts, give_range=False):
    global wins
    total = 0.0
    count = 0
    res = []
    c1 = itertools.permutations(decks_a)
    Ps = {}
    for l1 in c1:
        count += 1
        tmp = eval_one(l1, decks_b, win_pcts)
        total += tmp
        res.append((tmp, l1, decks_b))
    if give_range:
        return total / count, res
    return total / count

def eval_one(decks_a, decks_b, win_pcts):
    global wins
    total = 0
    assert len(decks_a) == len(decks_b) == 5, (len(decks_a), len(decks_b), decks_a)
    for outcome in wins:
        prod = 1.0
        for d1, d2, o in zip(decks_a, decks_b, outcome):
            if o == 1:
                prod *= win_pcts.get((d1, d2), 0.4999)
            else:
                prod *= (1 - win_pcts.get((d1, d2), 0.4999))
        total += prod
    return total

def eval_final_range(decks_a, decks_b, win_pcts):
    c1 = itertools.permutations(decks_a)
    c2 = itertools.permutations(decks_b)
    res = []
    for l1 in c1:
        for l2 in c2:
            tmp = 0
            for i, j in zip(l1, l2):
                tmp += get_win_pct(i, j, win_pcts)
            res.append(tmp / len(l1))
    return sorted(res)

debug = False

#P1 - Ban x2 
#P2 - Ban x2 
#P1 - Pick 
#P2 - Pick 
#P2 - Ban x2 
#P1 - Ban x2 
#P2 - Pick 
#P1 - Pick 
#P1 - Ban x1 
#P2 - Ban x1 
#P1 - Pick 
#P2 - Pick 

# ban 1a x2
# ban 1b x2
# pick 1a
# pick 1b
# ban 2b x2
# ban 2a x2
# pick 2b
# pick 2a
# ban 3a
# ban 3b
# pick 3a
# pick 3b

def ban1a(pool_a, pool_b, decks_a, decks_b, win_pcts, alpha=-10, beta=10, head=False, useAB=True):
    global eval_final, threshold
    bans_b = []
    possible_bans_b = list(itertools.combinations(pool_b,2))
    for p_b in possible_bans_b:
        p_b = list(p_b)
        tmp_pool_b = list(pool_b)
        for _i in p_b: tmp_pool_b.remove(_i)
        tmp_res = ban1b(pool_a, tmp_pool_b, decks_a, decks_b, win_pcts, alpha, beta, useAB=useAB)
        alpha = max(tmp_res[0], alpha)
        bans_b.append((tmp_res, p_b))
        if alpha >= beta + threshold and useAB:
            res = max(bans_b)
            return res[0][0], res
    res = max(bans_b)
    if head:
        for i,j in sorted(bans_b, reverse=True):
            print(j, i[0])
    return res[0][0], res

count = 0
def ban1b(pool_a, pool_b, decks_a, decks_b, win_pcts, alpha=-10, beta=10, head=False, useAB=True):
    global count
    count += 1
    print(count, datetime.datetime.now())
    #print(count, pool_a, pool_b, decks_a, decks_b)
    global eval_final, threshold
    bans_a = []
    possible_bans_a = list(itertools.combinations(pool_a,2))
    for p_a in possible_bans_a:
        p_a = list(p_a)
        tmp_pool_a = list(pool_a)
        for _i in p_a: tmp_pool_a.remove(_i)
        tmp_res = pick1a(tmp_pool_a, pool_b, decks_a, decks_b, win_pcts, alpha, beta, useAB=useAB)
        beta = min(tmp_res[0], beta)
        bans_a.append((tmp_res, p_a))
        if alpha >= beta + threshold and useAB:
            res = min(bans_a)
            return res[0][0], res
    res = min(bans_a)
    if head:
        for i,j in sorted(bans_a, reverse=False):
            print(j, i[0])
    return res[0][0], res

def pick1a(pool_a, pool_b, decks_a, decks_b, win_pcts, alpha=-10, beta=10, head=False, useAB=True):
    global eval_final, threshold
    picks_a = []
    possible_picks_a = list(itertools.combinations(pool_a,1))
    #possible_picks_a = pool_a
    picks_a = []
    for p_a in possible_picks_a:
        p_a = list(p_a)
        tmp_pool_a = list(pool_a)
        for _i in p_a: tmp_pool_a.remove(_i)
        tmp_res = pick1b(tmp_pool_a, pool_b, decks_a + p_a, decks_b, win_pcts, alpha, beta, useAB=useAB)
        alpha = max(tmp_res[0], alpha)
        picks_a.append((tmp_res, p_a))
        if alpha >= beta + threshold and useAB:
            res = max(picks_a)
            return res[0][0], res
    if head:
        for i,j in sorted(picks_a, reverse=True):
            print(j, i[0])
    res = max(picks_a)
    return res[0][0], res


def pick1b(pool_a, pool_b, decks_a, decks_b, win_pcts, alpha=-10, beta=10, head=False, useAB=True):
    #print(len(pool_a), len(pool_b), len(decks_a), len(decks_b))
    global eval_final, threshold
    picks_b = []
    possible_picks_b = list(itertools.combinations(pool_b,1))
    #possible_picks_b = pool_b
    for p_b in possible_picks_b:
        p_b = list(p_b)
        tmp_pool_b = list(pool_b)
        for _i in p_b: tmp_pool_b.remove(_i)
        tmp_res = ban2b(pool_a, tmp_pool_b, decks_a, decks_b + p_b, win_pcts, alpha, beta, useAB=useAB)
        beta = min(tmp_res[0], beta)
        picks_b.append((tmp_res, p_b))
        if alpha >= beta + threshold and useAB:
            res = min(picks_b)
            return res[0][0], res
    if head:
        for i,j in sorted(picks_b, reverse=False):
            print(j, i[0])
    res = min(picks_b)
    return res[0][0], res


def ban2b(pool_a, pool_b, decks_a, decks_b, win_pcts, alpha=-10, beta=10, head=False, useAB=True):
    #print(len(pool_a), len(pool_b), len(decks_a), len(decks_b))
    global eval_final, threshold
    bans_a = []
    possible_bans_a = list(itertools.combinations(pool_a,2))
    for p_a in possible_bans_a:
        p_a = list(p_a)
        tmp_pool_a = list(pool_a)
        for _i in p_a: tmp_pool_a.remove(_i)
        tmp_res = ban2a(tmp_pool_a, pool_b, decks_a, decks_b, win_pcts, alpha, beta, useAB=useAB)
        beta = min(tmp_res[0], beta)
        bans_a.append((tmp_res, p_a))
        if alpha >= beta + threshold and useAB:
            res = min(bans_a)
            return res[0][0], res
    res = min(bans_a)
    if head:
        for i,j in sorted(bans_a, reverse=False):
            print(j, i[0])
    return res[0][0], res

def ban2a(pool_a, pool_b, decks_a, decks_b, win_pcts, alpha=-10, beta=10, head=False, useAB=True):
    global eval_final, threshold
    bans_b = []
    possible_bans_b = list(itertools.combinations(pool_b,2))
    for p_b in possible_bans_b:
        p_b = list(p_b)
        tmp_pool_b = list(pool_b)
        for _i in p_b: tmp_pool_b.remove(_i)
        tmp_res = pick2b(pool_a, tmp_pool_b, decks_a, decks_b, win_pcts, alpha, beta, useAB=useAB)
        alpha = max(tmp_res[0], alpha)
        bans_b.append((tmp_res, p_b))
        if alpha >= beta + threshold and useAB:
            res = max(bans_b)
            return res[0][0], res
    res = max(bans_b)
    if head:
        for i,j in sorted(bans_b, reverse=True):
            print(j, i[0])
    return res[0][0], res


def pick2b(pool_a, pool_b, decks_a, decks_b, win_pcts, alpha=-10, beta=10, head=False, useAB=True):
    #print(len(pool_a), len(pool_b), len(decks_a), len(decks_b))
    global eval_final, threshold
    picks_b = []
    possible_picks_b = list(itertools.combinations(pool_b,1))
    #possible_picks_b = pool_b
    for p_b in possible_picks_b:
        p_b = list(p_b)
        tmp_pool_b = list(pool_b)
        for _i in p_b: tmp_pool_b.remove(_i)
        tmp_res = pick2a(pool_a, tmp_pool_b, decks_a, decks_b + p_b, win_pcts, alpha, beta, useAB=useAB)
        beta = min(tmp_res[0], beta)
        picks_b.append((tmp_res, p_b))
        if alpha >= beta + threshold and useAB:
            res = min(picks_b)
            return res[0][0], res
    res = min(picks_b)
    if head:
        for i,j in sorted(picks_b, reverse=False):
            print(j, i[0])
    return res[0][0], res

def pick2a(pool_a, pool_b, decks_a, decks_b, win_pcts, alpha=-10, beta=10, head=False, useAB=True):
    global eval_final, threshold
    picks_a = []
    possible_picks_a = list(itertools.combinations(pool_a,1))
    #possible_picks_a = pool_a
    for p_a in possible_picks_a:
        p_a = list(p_a)
        tmp_pool_a = list(pool_a)
        for _i in p_a: tmp_pool_a.remove(_i)
        tmp_res = ban3a(tmp_pool_a, pool_b, decks_a + p_a, decks_b, win_pcts, alpha, beta, useAB=useAB)
        alpha = max(tmp_res[0], alpha)
        picks_a.append((tmp_res, p_a))
        if alpha >= beta + threshold and useAB:
            res = max(picks_a)
            return res[0][0], res
    res = max(picks_a)
    if head:
        for i,j in sorted(picks_a, reverse=True):
            print(j, i[0])
    return res[0][0], res

def ban3a(pool_a, pool_b, decks_a, decks_b, win_pcts, alpha=-10, beta=10, head=False, useAB=True):
    global eval_final, threshold
    bans_b = []
    possible_bans_b = list(itertools.combinations(pool_b,1))
    #possible_bans_b = pool_b
    for p_b in possible_bans_b:
        p_b = list(p_b)
        tmp_pool_b = list(pool_b)
        for _i in p_b: tmp_pool_b.remove(_i)
        tmp_res = ban3b(pool_a, tmp_pool_b, decks_a, decks_b, win_pcts, alpha, beta, useAB=useAB)
        alpha = max(tmp_res[0], alpha)
        bans_b.append((tmp_res, p_b))
        if alpha >= beta + threshold and useAB:
            res = max(bans_b)
            return res[0][0], res
    res = max(bans_b)
    if head:
        for i,j in sorted(bans_b, reverse=True):
            print(j, i[0])
    return res[0][0], res

def ban3b(pool_a, pool_b, decks_a, decks_b, win_pcts, alpha=-10, beta=10, head=False, useAB=True):
    global eval_final, threshold
    bans_a = []
    possible_bans_a = list(itertools.combinations(pool_a,1))
    #possible_bans_a = pool_a
    for p_a in possible_bans_a:
        p_a = list(p_a)
        tmp_pool_a = list(pool_a)
        for _i in p_a: tmp_pool_a.remove(_i)
        tmp_res = pick3a(tmp_pool_a, pool_b, decks_a, decks_b, win_pcts, alpha, beta, useAB=useAB)
        beta = min(tmp_res[0], beta)
        bans_a.append((tmp_res, p_a))
        if alpha >= beta + threshold and useAB:
            res = min(bans_a)
            return res[0][0], res
    res = min(bans_a)
    if head:
        for i,j in sorted(bans_a, reverse=False):
            print(j, i[0])
    return res[0][0], res

def pick3a(pool_a, pool_b, decks_a, decks_b, win_pcts, alpha=-10, beta=10, head=False, useAB=True):
    global eval_final, threshold
    picks_a = []
    possible_picks_a = list(itertools.combinations(pool_a,1))
    #possible_picks_a = pool_a
    for p_a in possible_picks_a:
        p_a = list(p_a)
        tmp_pool_a = list(pool_a)
        for _i in p_a: tmp_pool_a.remove(_i)
        tmp_res = pick3b(tmp_pool_a, pool_b, decks_a + p_a, decks_b, win_pcts, alpha, beta, useAB=useAB)
        alpha = max(tmp_res[0], alpha)
        picks_a.append((tmp_res, p_a))
        if alpha >= beta + threshold and useAB:
            res = max(picks_a)
            return res[0][0], res
    res = max(picks_a)
    if head:
        for i,j in sorted(picks_a, reverse=True):
            print(j, i[0])
    return res[0][0], res

def pick3b(pool_a, pool_b, decks_a, decks_b, win_pcts, alpha=-10, beta=10, head=False, useAB=True):
    global eval_final, threshold
    picks_b = []
    possible_picks_b = list(itertools.combinations(pool_b,1))
    #possible_picks_a = pool_a
    for p_b in possible_picks_b:
        p_b = list(p_b)
        tmp_res = eval_final(decks_a, decks_b + p_b, win_pcts)
        beta = min(tmp_res, beta)
        picks_b.append((tmp_res, (p_b, decks_a, decks_b + p_b)))
        if alpha >= beta + threshold and useAB:
            res = min(picks_b)
            return res[0], res
    res = min(picks_b)
    if head:
        for i,j in sorted(picks_b, reverse=False):
            print(j, i)
    return res[0], res

if __name__ == '__main__':
    from json_win_rates import *
    #BUL
    #l1 = "Odd Warrior,Mecha'thun Priest,Shudderwock Shaman,Even Warlock,Odd Paladin,Quest Rogue,Big Spell Mage,Token Druid,Deathrattle Hunter".split(',')
    #l2 = "Odd Warrior,Control Priest,Shudderwock Shaman,Even Warlock,OTK DK Paladin,Quest Rogue,Tempo Mage,Mill Druid,Deathrattle Hunter".split(',')

    #USA
    #l1 = "Odd Warrior,USA Control Priest,Shudderwock Shaman,Even Warlock,Even Paladin,Quest Rogue,Tempo Mage,Token Druid,Deathrattle Hunter".split(',')
    #l2 = "Odd Warrior,TWN Control Priest,Shudderwock Shaman,Even Warlock,Odd Paladin,Odd Rogue,Tempo Mage,Mill Druid,Deathrattle Hunter".split(',')
    
    #l1 = "Malygos Druid,Spell Hunter,Murloc Mage,Even Paladin,Clone Priest,Quest Rogue,Shudderwock Shaman,Even Warlock,Odd Warrior".split(',')
    #l2 = "Taunt Druid,Secret Hunter,Tempo Mage,Odd Paladin,Control Priest,Kingsbane Rogue,Even Shaman,Even Warlock,Odd Warrior".split(',')
    l1 = "Shudderwock Shaman,Malygos Druid,Quest Rogue,Control Priest,Deathrattle Hunter,Murloc Mage,Zoo Warlock,Even Paladin,Odd Warrior".split(',')
    #l2 = "Shudderwock Shaman,Malygos Druid,Quest Rogue,Control Priest,Deathrattle Hunter,Murloc Mage,Zoo Warlock,Even Paladin,Odd Warrior".split(',')
    l2 = "Odd Warrior,Even Warlock,Shudderwock Shaman,Kingsbane Rogue,Control Priest,Odd Paladin,Tempo Mage,Secret Hunter,Malygos Druid".split(',')
    
    win_pcts, num_games, game_count, archetypes, overall_wr = get_win_pcts(min_game_threshold=0, min_game_count=0,limitTop=100)
    assert all([d in archetypes for d in l1]), ([d in archetypes for d in l1], l1)
    assert all([d in archetypes for d in l2]), ([d in archetypes for d in l2], l2)
    #l2 = "Token Druid,Deathrattle Hunter,Murloc Mage,Odd Paladin,Clone Priest,Quest Rogue,Shudderwock Shaman,Cube Warlock,Odd Quest Warrior".split(',')
    #l1 = l1.shuffle()

    #debug = True
    mu = WSOE_Matchup(l1, l2, win_pcts=None)
    if True:
        initialize(l1, l2, mu.win_pcts)
        #mu.add_ban([], ['Deathrattle Hunter', 'Odd Warrior'])
        print(mu.calculate())
    if False:
        initialize(l1, l2, mu.win_pcts)
        #draft 1
        #mu.add_ban(['Malygos Druid', 'Spell Hunter'],['Taunt Druid', 'Secret Hunter'])
        mu.calculate()
        print("")
        mu.add_ban([],['Taunt Druid', 'Secret Hunter'])
        mu.calculate()
        print("")
        mu.add_ban(['Malygos Druid', 'Spell Hunter'],[])
        mu.calculate()
        print("")
        mu.add_picks(['Quest Rogue'])
        mu.calculate()
        print("")
        mu.add_picks([], ['Even Warlock'])
        mu.calculate()
        print("")
        mu.add_ban(['Clone Priest', 'Even Warlock'], [])
        mu.calculate()
        print("")
        mu.add_ban([], ['Tempo Mage', 'Odd Paladin'])
        mu.calculate()
        print("")
        mu.add_picks([], ['Even Shaman'])
        mu.calculate()
        print("")
        mu.add_picks(['Odd Warrior'])
        mu.calculate()
        print("")
        mu.add_ban([],['Odd Warrior'])
        mu.calculate()
        print("")
        mu.add_ban(['Shudderwock Shaman'],[])
        mu.calculate()
        print("")
        mu.add_picks(['Murloc Mage'])
        #mu.add_ban([],['Malygos Druid', 'Spell Hunter'])
        print(mu.calculate())
    #draft 2
    #mu.add_ban(['Quest Rogue', 'Shudderwock Shaman'],['Taunt Druid', 'Secret Hunter'])
    #mu.calculate()
    #print("")
    #mu.add_picks(['Spell Hunter'])
    #mu.calculate()
    #print("")
    #mu.add_picks([], ['Odd Paladin'])
    #mu.calculate()
    #print("")
    #mu.add_ban(['Even Warlock', 'Odd Warrior'], [])
    #mu.calculate()
    #print("")
    #mu.add_ban([], ['Kingsbane Rogue', 'Odd Warrior'])
    #mu.calculate()
    #print("")
    #mu.add_picks([], ['Even Warlock'])
    #mu.calculate()
    #print("")
    #mu.add_picks(['Clone Priest'])
    #mu.calculate()
    #print("")
    #mu.add_ban([],['Even Shaman'])
    #mu.calculate()
    #print("")
    #mu.add_ban(['Malygos Druid'],[])
    #mu.calculate()
    #print("")
    #mu.add_picks(['Even Paladin'])
    #mu.add_ban([],['Malygos Druid', 'Spell Hunter'])
    #print(mu.calculate())

    
    #archetype_set = set(l1)
    #archetype_set = archetype_set.union(set(l2))
    #archetype_map = {}
    #archetype_map_inv = {}
    #win_pcts_int = {}
    #for index, a1 in zip(range(0, len(archetype_set)), archetype_set):
    #    archetype_map[index] = a1
    #    archetype_map_inv[a1] = index
    #for i, a_i in archetype_map.items():
    #    for j, a_j in archetype_map.items():
    #        win_pcts_int[(i,j)] = mu.win_pcts.get((a_i,a_j), 0.4999)
    #pool_a_int = [archetype_map_inv[a] for a in l1]
    #pool_b_int = [archetype_map_inv[a] for a in l2]
    #initialize(pool_a_int, pool_b_int, win_pcts_int)
    #mu = WSOE_Matchup(pool_a_int, pool_b_int, win_pcts=win_pcts_int)
    #print(mu.calculate())
