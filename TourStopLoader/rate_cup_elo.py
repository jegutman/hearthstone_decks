import sys
sys.path.append('../')
from config import basedir
sys.path.append(basedir)
sys.path.append(basedir + '/lineupSolver')
sys.path.append(basedir + '/TourStopLoader')
from hs_elo import *
import datetime
import math

offline_tournaments = [
]

import MySQLdb
import MySQLdb.constants as const
from config import *
connection = MySQLdb.connect(host='localhost', user=db_user, passwd=db_passwd, charset = 'utf8mb4')
#connection = MySQLdb.connect(user = 'guest', db = 'test', charset = 'utf8')
cursor = connection.cursor()
cursor.execute("SET NAMES utf8")

def logloss(result, predicted, eps=1e-15):
    if result == 1:
        return -math.log(predicted)
    else:
        return -math.log(1 - predicted)

#for K in range(16, 64, 4):
K = 36
tournaments = set()
env = HS_Elo(defaultK=K)

#HCT German TakeTV (S1),Global Qualifier,1,Sintolol,Radogask,3,1
#event,sub_event,
rating = {}
rating_games = {}
wins = {}
expected = []
errors = []
baseline = []
bucket_pred = {}
bucket_res = {}
        
db = 'masters_cups'
sql = """SELECT p1.player_name, p2.player_name, g.result 
         FROM %(db)s.games g join %(db)s.player_info p1 on g.tournament_id = p1.tournament_id and g.player_id = p1.player_id
                             join %(db)s.player_info p2 on g.tournament_id = p2.tournament_id and g.opponent_id = p2.player_id
                             join %(db)s.tournament t on g.tournament_id = t.tournament_id
         WHERE result = 'W'
         ORDER BY time, round_number
      """
print(sql % locals())
cursor.execute(sql % locals())
for p1, p2, result in cursor.fetchall():
    #event, sub_event, sub_bracket, date, season, patch, round_num, p1, p2, score1, score2 = line.strip().split(',')
    #round_num, p1, p2, score1, score2 = line
    #print(date)
    #if date < '2018_07_01': continue
    # EXCLUDE ONLINE
    #if int(season) != 3: continue
    p1 = p1.lower()
    p2 = p2.lower()
    result = 1
    rating_games[p1] = rating_games.get(p1, 0) + 1
    rating_games[p2] = rating_games.get(p2, 0) + 1
    if p1 not in rating:
        rating[p1] = env.create_rating()
    if p2 not in rating:
        rating[p2] = env.create_rating()
    #print(env.quality_1vs1(rating[p1], rating[p2]))
    est = env.expect_score(rating[p1], rating[p2])
    #if min(rating_games[p1], rating_games[p2]) >= 10:
    if min(rating_games[p1], rating_games[p2]) >= 10 and min(rating[p1].mu, rating[p2].mu) > 1700:
        bucket = round(est * 2, 1) / 2.
        bucket_pred[bucket] = bucket_pred.get(bucket, []) + [est]
        bucket_res[bucket] = bucket_res.get(bucket, []) + [1 if result else 0]
    expected.append( est)
    #baseline.append((0.5-result)**2)
    if result:
        env.rate_1vs1(rating[p1], rating[p2])
        wins[p1] = wins.get(p1, 0) + 1
        #if min(rating_games[p1], rating_games[p2]) >= 10:
        #    error = (est - 1) ** 2
    else:
        env.rate_1vs1(rating[p2], rating[p1])
        wins[p2] = wins.get(p2, 0) + 1
        #if min(rating_games[p1], rating_games[p2]) >= 10:
        #    error = (est - 0) ** 2
    if min(rating_games[p1], rating_games[p2]) >= 10:
        error = logloss(result, est)
        errors.append(error)

min_games = 15

def expose(r):
    return int(r.mu)

if __name__ == '__main__':
    top_players = [i for i in sorted(rating.items(), key = lambda x:expose(x[1]), reverse=True) if rating_games[i[0]] >= min_games]
    #top_players = [i for i in sorted(rating.items(), key = lambda x:expose(x[1]), reverse=True) if rating_games[i[0]] < 60]
    if True:
        print("   %-15s %-5s %-5s" % ('Player', 'rEst', 'games'))
        index = 0
        for p, r in top_players[:50]:
            index += 1
            win = wins.get(p, 0)
            losses = rating_games[p] - win
            pct = int(100 * win / float(rating_games[p]))
            print("%2s %-15s %5s %4s    %3s - %-3s   %s%%" % (index, p, expose(r), rating_games[p], win, losses, pct))

    print('')
    print(K, round(sum(errors) / len(errors), 5))

    
    total_mini_error = 0
    count = 0
    #for bucket in sorted(bucket_pred.keys()):
    #    if 0.3 <= bucket <= 0.7:
    #        a = sum(bucket_pred[bucket]) / len(bucket_pred[bucket])
    #        b = sum(bucket_res[bucket]) / len(bucket_res[bucket])
    #        c = len(bucket_res[bucket])
    #        total_mini_error += (a - b) ** 2 * c
    #        count += c
    #    print("%-4.2f" % bucket,"%-5.3f" % round(sum(bucket_pred[bucket]) / len(bucket_pred[bucket]), 3),"%-5.3f" % round(sum(bucket_res[bucket]) / len(bucket_res[bucket]), 3), len(bucket_res[bucket]))
    #print("mini_error", round(total_mini_error / count * 100, 3))
    for bucket in sorted(bucket_pred.keys()):
        if bucket < 0.5:
            continue
            #a = sum(bucket_pred[bucket]) / len(bucket_pred[bucket])
            a = sum(bucket_pred[bucket] + bucket_pred[1-bucket]) / len(bucket_pred[bucket] + bucket_pred[1-bucket])
            b = sum(bucket_res[bucket] + bucket_pred[1-bucket]) / len(bucket_res[bucket] + bucket_pred[1-bucket])
            c = len(bucket_res[bucket])
        print("%-4.2f" % bucket,"%-5.3f" % round(sum(bucket_pred[bucket]) / len(bucket_pred[bucket]), 3),"%-5.3f" % round(sum(bucket_res[bucket]) / len(bucket_res[bucket]), 3), len(bucket_res[bucket]))
