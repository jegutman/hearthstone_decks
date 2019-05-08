from collections import defaultdict
s1 = {}
s2 = {}
s3 = {}
total = defaultdict(lambda:0)
s1_file = open('season1.csv')
for line in s1_file:
    player, pts = line.strip().split(',')
    s1[player] = int(pts)
    total[player] += int(pts)
s2_file = open('season2.csv')
for line in s2_file:
    player, pts = line.strip().split(',')
    s2[player] = int(pts)
    total[player] += int(pts)
s3_file = open('season3.csv')
for line in s3_file:
    player, pts = line.strip().split(',')
    s3[player] = int(pts)
    total[player] += int(pts)

for player, tpts in sorted(total.items(), key=lambda x:x[1], reverse=True):
    a,b,c = s1.get(player, 0), s2.get(player,0), s3.get(player,0)
    print("%s,%s,%s,%s,%s" % (player, a,b,c, tpts))
