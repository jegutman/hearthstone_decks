import sys
sys.path.append('../')
from config import basedir
sys.path.append(basedir)
sys.path.append(basedir + '/lineupSolver')
from shared_utils import *
import itertools
from pprint import pprint

class HGG_Matchup():
    def __init__(self, l1, l2, decksA=[], decksB=[], win_pcts = None, clear_initialize=False):
        self.poolA = list(l1)
        self.poolB = list(l2)
        self.decksA = decksA
        self.decksB = decksB
        if not win_pcts:
            self.win_pcts = get_win_pcts(min_game_threshold=0, min_game_count=0,limitTop=100)[0]
        else:
            self.win_pcts = win_pcts
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

    def calculate(self, isGoofy=False):
        poolA = self.poolA
        poolB = self.poolB
        decksA = self.decksA
        decksB = self.decksB
        if isGoofy:
            poolA, poolB = poolB, poolA
            decksA, decksB = decksB, decksA
        assert len(poolA) == len(poolB), "pools must be equal in size"
        assert len(decksA) == len(decksB), "decks must be equal in size"
        if len(poolA) == 9:
            print("ban1")
            return ban1_int(poolA, poolB, self.win_pcts)
        elif len(poolA) == 8:
            print("pick1")
            return pick1_int(poolA, poolB, self.win_pcts)
        elif len(poolA) == 6 and len(decksA) == 2:
            print("ban2")
            return ban2(poolA, poolB, decksA, decksB, self.win_pcts)
        elif len(poolA) == 4 and len(decksA) == 2:
            print("pick2")
            return pick2(poolA, poolB, decksA, decksB, self.win_pcts)
        elif len(poolA) == 2 and len(decksA) == 4:
            print("ban3")
            return ban3(poolA, poolB, decksA, decksB, self.win_pcts)
        else:
            return "Unexpected State"
            
        
        

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
    print(decks_a, decks_b)
    res = {}
    #decks_a = sorted(decks_a, key=lambda x:x.split(' ')[-1])
    #decks_b = sorted(decks_b, key=lambda x:x.split(' ')[-1])
    decks_a = sorted(decks_a)
    decks_b = sorted(decks_b)
    all_l1 = list(itertools.combinations(decks_a, 5))
    all_l2 = list(itertools.combinations(decks_b, 5))
    count = 0
    print("Initializing", len(all_l1) * len(all_l2))
    print("len", len(list(all_l1)), len(list(all_l2)))
    for l1 in all_l1:
        for l2 in all_l2:
            count += 1
            if debug:
                if count % 1000 == 0:
                    print(count)
            res[(tuple(l1), tuple(l2))] = eval_final_calc(l1, l2, win_pcts)
            res[(tuple(l2), tuple(l1))] = 1 - res[(tuple(l1), tuple(l2))]
    #print(res)
    win_rates_init = res
    def eval_final_tmp(decks_a, decks_b, win_pcts):
        decks_a = sorted(decks_a)
        decks_b = sorted(decks_b)
        return round(res[(tuple(decks_a), tuple(decks_b))], 6)
    global eval_final
    print("Done Initializing")
    eval_final = eval_final_tmp

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

###
# Ban 1 (1 deck)
# Pick 1 (2 decks)
# Ban 2 (2 decks)
# Pick 2 (2 decks)
# Ban 3 (1 deck)

debug = False
def ban3(pool_a, pool_b, decks_a, decks_b, win_pcts):
    global eval_final
    if not eval_final:
        initialize(pool_a+decks_a, pool_b+decks_b, win_pcts)
    bans1 = []
    for p1_ban in pool_b:
        bans2 = []
        tmp_pool_b = list(pool_b)
        tmp_pool_b.remove(p1_ban)
        for p2_ban in pool_a:
            tmp_pool_a = list(pool_a)
            tmp_pool_a.remove(p2_ban)
            bans2.append((eval_final(decks_a + tmp_pool_a, decks_b + tmp_pool_b, win_pcts), p2_ban))
        bans1.append((min(bans2), p1_ban))
    global debug
    res = max(bans1)
    #print(bans1)
    return res[0][0], res

def pick2(pool_a, pool_b, decks_a, decks_b, win_pcts):
    global eval_final
    if not eval_final:
        initialize(pool_a+decks_a, pool_b+decks_b, win_pcts)
    picks_a = []
    possible_picks_a = list(itertools.combinations(pool_a,2))
    possible_picks_b = list(itertools.combinations(pool_b,2))
    for p_a in possible_picks_a:
        p_a = list(p_a)
        picks_b = []
        tmp_pool_a = list(pool_a)
        for _i in p_a: tmp_pool_a.remove(_i)
        for p_b in possible_picks_b:
            p_b = list(p_b)
            tmp_pool_b = list(pool_b)
            for _i in p_b: tmp_pool_b.remove(_i)
            picks_b.append((ban3(tmp_pool_a, tmp_pool_b, decks_a + p_a, decks_b + p_b, win_pcts)[0], p_b))
        picks_a.append((min(picks_b), p_a))
    res = max(picks_a)
    return res[0][0], res
    
debug=False
def ban2(pool_a, pool_b, decks_a, decks_b, win_pcts):
    global eval_final, debug
    if not eval_final:
        initialize(pool_a+decks_a, pool_b+decks_b, win_pcts)
    bans_from_b = []
    possible_bans_from_b = list(itertools.combinations(pool_b,2))
    possible_bans_from_a = list(itertools.combinations(pool_a,2))
    for p_b in possible_bans_from_b:
        p_b = list(p_b)
        bans_from_a = []
        tmp_pool_b = list(pool_b)
        for _i in p_b: tmp_pool_b.remove(_i)
        for p_a in possible_bans_from_a:
            p_a = list(p_a)
            tmp_pool_a = list(pool_a)
            for _i in p_a: tmp_pool_a.remove(_i)
            bans_from_a.append((pick2(tmp_pool_a, tmp_pool_b, decks_a, decks_b, win_pcts)[0], p_a))
        bans_from_b.append((min(bans_from_a), p_b))
    if debug:
        print(bans_from_b)
    res = max(bans_from_b)
    return res[0][0], res

def convert(archetype_map):
    pass

def pick1_int(pool_a, pool_b, win_pcts):
    global eval_final
    archetype_set = set(pool_a)
    archetype_set = archetype_set.union(set(pool_b))
    archetype_map = {}
    archetype_map_inv = {}
    win_pcts_int = {}
    for index, a1 in zip(range(0, len(archetype_set)), archetype_set):
        archetype_map[index] = a1
        archetype_map_inv[a1] = index
    for i, a_i in archetype_map.items():
        for j, a_j in archetype_map.items():
            win_pcts_int[(i,j)] = win_pcts.get((a_i,a_j), 0.4999)
    pool_a_int = [archetype_map_inv[a] for a in pool_a]
    pool_b_int = [archetype_map_inv[a] for a in pool_b]
    if not eval_final:
        initialize(pool_a_int, pool_b_int, win_pcts_int)
    return pick1(pool_a_int, pool_b_int, win_pcts_int), archetype_map

def avg_win_pct(deck1, deck_pool, win_pcts):
    total = 0.0
    count = 0
    for i in deck_pool:
        total += win_pcts[(deck1, i)]
        count += 1
    return round(total / count, 4)

def pick1(pool_a, pool_b, win_pcts):
    picks_a = []
    count = 0
    pool_a = sorted(pool_a, key=lambda x:avg_win_pct(x, pool_b, win_pcts), reverse=True)
    pool_b = sorted(pool_b, key=lambda x:avg_win_pct(x, pool_a, win_pcts), reverse=True)
    prune = 0
    for x_a in range(0, len(pool_a)-1):
        for y_a in range(x_a+1, len(pool_a)):
            p_a = [pool_a[x_a], pool_a[y_a]]
            picks_b = []
            tmp_pool_a = list(pool_a)
            for _i in p_a: tmp_pool_a.remove(_i)
            possible_picks_b = list(itertools.combinations(pool_b,2))
            for x_b in range(0, len(pool_b)-1):
                if len(picks_b) > 0 and len(picks_a) > 0:
                    if min(picks_b)[0] < max(picks_a)[0][0]:
                        prune += 1
                        #print("pruned %s" % prune)
                        continue
                for y_b in range(x_b+1, len(pool_b)):
                    count += 1
                    p_b = [pool_b[x_b], pool_b[y_b]]
                    #print(count, p_b)
                    tmp_pool_b = list(pool_b)
                    for _i in p_b: tmp_pool_b.remove(_i)
                    tmp_res = ban2(tmp_pool_a, tmp_pool_b, p_a, p_b, win_pcts)[0]
                    picks_b.append((tmp_res, p_b))
                    
            picks_a.append((min(picks_b), p_a))
    res = max(picks_a)
    return res[0][0], res

def ban1_int(pool_a, pool_b, win_pcts):
    global eval_final
    archetype_set = set(pool_a)
    archetype_set = archetype_set.union(set(pool_b))
    archetype_map = {}
    archetype_map_inv = {}
    win_pcts_int = {}
    for index, a1 in zip(range(0, len(archetype_set)), archetype_set):
        archetype_map[index] = a1
        archetype_map_inv[a1] = index
    for i, a_i in archetype_map.items():
        for j, a_j in archetype_map.items():
            win_pcts_int[(i,j)] = win_pcts.get((a_i,a_j), 0.4999)
    pool_a_int = [archetype_map_inv[a] for a in pool_a]
    pool_b_int = [archetype_map_inv[a] for a in pool_b]
    if not eval_final:
        initialize(pool_a_int, pool_b_int, win_pcts_int)
    return ban1(pool_a_int, pool_b_int, win_pcts_int), archetype_map

def ban1(pool_a, pool_b, win_pcts):
    bans_from_b = []
    pool_a = sorted(pool_a, key=lambda x:avg_win_pct(x, pool_b, win_pcts), reverse=True)
    pool_b = sorted(pool_b, key=lambda x:avg_win_pct(x, pool_a, win_pcts), reverse=True)
    possible_bans_from_b = pool_b
    possible_bans_from_a = pool_a
    print(possible_bans_from_a, possible_bans_from_b)
    count = 0
    prune = 0
    for p_b in possible_bans_from_b:
        bans_from_a = []
        tmp_pool_b = list(pool_b)
        tmp_pool_b.remove(p_b)
        for p_a in possible_bans_from_a:
            if len(bans_from_b) > 0 and len(bans_from_a) > 0:
                #print(min(bans_from_a)[0], max(bans_from_b)[0][0])
                if min(bans_from_a)[0] < max(bans_from_b)[0][0]:
                    prune += 1
                    print(prune, "pruned")
                    continue
            count += 1
            print(count, 'ban1', p_a, p_b)
            tmp_pool_a = list(pool_a)
            tmp_pool_a.remove(p_a)
            bans_from_a.append((pick1(tmp_pool_a, tmp_pool_b, win_pcts)[0], p_a))
        bans_from_b.append((min(bans_from_a), p_b))
    return max(bans_from_b), bans_from_b

if __name__ == '__main__':
    from json_win_rates import *
    #l1 = ['Malygos Druid', 'Recruit Hunter', 'Tempo Mage', 'Odd Paladin', 'Control Priest', 'Miracle Rogue', 'Shudderwock Shaman', 'Cube Warlock', 'Quest Warrior']
    #l2 = ['Malygos Druid', 'Spell Hunter', 'Big Spell Mage', 'Odd Paladin', 'Control Priest', 'Odd Rogue', 'Shudderwock Shaman', 'Cube Warlock', 'Quest Warrior']
    #l1 = "Shudderwock Shaman,Odd Paladin,Mill Druid,Murloc Mage,Zoo Warlock,Combo Priest,Odd Rogue,Deathrattle Hunter,Quest Warrior".split(',')
    #l2 = "Quest Warrior,Control Priest,Shudderwock Shaman,Even Warlock,Odd Paladin,Odd Rogue,Tempo Mage,Malygos Druid,Deathrattle Hunter".split(',')
    l1 = "Quest Warrior,Quest Priest,Shudderwock Shaman,Zoo Warlock,Odd Paladin,Odd Rogue,Murloc Mage,Token Druid,Deathrattle Hunter".split(',')
    l2 = "Quest Warrior,Control Priest,Even Shaman,Zoo Warlock,Odd Paladin,Miracle Rogue,Tempo Mage,Malygos Druid,Deathrattle Hunter".split(',')
    #debug = True
    mu = HGG_Matchup(l1, l2)
    mu.add_ban(['Zoo Warlock'], ['Odd Paladin'])
    #mu.add_picks(['Deathrattle Hunter', 'Shudderwock Shaman'], ['Odd Paladin', 'Control Priest'])
    #mu.add_ban(['Combo Priest', 'Quest Warrior'], ['Odd Rogue', 'Deathrattle Hunter'])
    #mu.add_picks(['Odd Paladin', 'Zoo Warlock'], ['Malygos Druid', 'Shudderwock Shaman'])
    #mu.add_picks(['Murloc Mage', 'Zoo Warlock'], ['Quest Warrior', 'Shudderwock Shaman'])
    #mu.add_ban(['Malygos Druid'], ['Malygos Druid'])
    tmp = mu.calculate(isGoofy=True)
    #tmp = mu.calculate()
    print('\n', tmp)
