# some assumptions on formating
# whatever deck a player is forced to play should be listed first (for 3v2 and 2v2 scenarios, irrelevant otherwise)

# branching calcs
# 16 x ban phase
# 9x first deck pick
# 2x first loss
# ~2x second player loss

# "real" lineup
win_pct = {
    ('rogue', 'rogue')   : 0.5,
    ('zoo', 'zoo')       : 0.5,
    ('druid', 'druid')   : 0.5,
    ('priest', 'priest') : 0.5,
    ('murloc', 'murloc') : 0.5,
    ('rogue', 'priest')  : 0.452,
    ('rogue', 'zoo')     : 0.530,
    ('rogue', 'druid')   : 0.505,
    ('rogue', 'murloc')  : 0.539,
    ('rogue', 'bpriest') : 0.504,
    ('rogue', 'bdruid')  : 0.504,
    ('priest', 'zoo')    : 0.498,
    ('priest', 'druid')  : 0.427,
    ('priest', 'murloc') : 0.507,
    ('priest', 'bpriest'): 0.501,
    ('priest', 'bdruid') : 0.352,
    ('zoo', 'druid')     : 0.521,
    ('zoo', 'murloc')    : 0.511,
    ('zoo', 'bpriest')   : 0.424,
    ('zoo', 'bdruid')    : 0.480,
    ('druid', 'murloc')  : 0.456,
    ('druid', 'bdruid')  : 0.426,
    ('druid', 'bpriest') : 0.563,
    ('bpriest', 'bdruid'): 0.492,
    ('bpriest', 'murloc'): 0.601,
    ('bdruid', 'murloc'): 0.404,
}

print "win_pcts"
for i, j in sorted(win_pct.items()):
    d1, d2 = i
    print '%-8s %-8s %s' % (d1, d2, j)


for pair in win_pct.keys():
    i,j = pair
    if (j,i) not in win_pct:
        win_pct[(j,i)] = 1 - win_pct[(i,j)]

def get_win_pct(a,b, win_pcts):
    return win_pcts[(a,b)]

def post_pick(decks_a, decks_b, win_pcts, a_pick=None, b_pick=None):
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
        return res

#lineup_1 = ['rogue', 'druid', 'priest', 'zoo']
#lineup_2 = ['rogue', 'druid', 'priest', 'murloc']
#res = pre_ban(lineup_1,
#              lineup_2,
#              win_pct)
#print ""
#print lineup_1, "vs", lineup_2
#print "bans"
#print "%-8s %-8s" % ("p1_ban", "p2_ban")
#for i, j in sorted(res.items(), key=lambda x:-x[1]):
#    d1, d2 = i
#    print '%-8s %-8s %s' % (d1, d2, round(j,4))

#lineup_1 = ['rogue', 'druid', 'zoo']
#lineup_1 = ['priest', 'druid', 'zoo']
#lineup_2 = ['priest', 'druid', 'murloc']
#lineup_1 = ['rogue', 'bpriest', 'zoo']
#lineup_1 = ['rogue', 'priest', 'druid']
lineup_1 = ['bpriest']
lineup_2 = ['druid', 'murloc']
print lineup_1, "vs", lineup_2
print "lead"
print "%-8s %-8s" % ("p1_lead", "p2_lead")
all_res = []
for i in lineup_1:
    for j in lineup_2:
        res = post_pick(lineup_1,
                        lineup_2,
                        win_pct, i, j)
        all_res.append(res)
        print '%-8s %-8s %s' % (i, j, round(res, 4))
print "average:", round(sum(all_res) / len(all_res), 4)

lineup_1 = ['rogue', 'bpriest', 'bdruid', 'zoo']
#lineup_1 = ['rogue',  'priest',  'druid', 'zoo']
lineup_2 = ['rogue',  'priest',  'druid', 'zoo']

print lineup_1, "vs", lineup_2
print "ban"
print "%-8s %-8s" % ("p1_ban", "p2_ban")
all_res = []
for y in lineup_2:
    for x in lineup_1:
        tmp_a = lineup_1[:]
        tmp_b = lineup_2[:]
        tmp_a.remove(x)
        tmp_b.remove(y)
        for i in tmp_a:
            for j in tmp_b:
                res = post_pick(tmp_a,
                                tmp_b,
                                win_pct, i, j)
                all_res.append(res)
                #print '%-8s %-8s %s' % (i, j, round(res, 4))
        print "%-8s %-8s" % (y,x),
        print "average:", round(sum(all_res) / len(all_res), 4)
