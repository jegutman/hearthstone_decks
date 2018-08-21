from hs_elo import *
import math

def logloss(result, predicted, eps=1e-15):
    if result == 1:
        return -math.log(predicted)
    else:
        return -math.log(1 - predicted)

#for K in range(16, 64, 4):
for K in range(36, 38, 2):
    env = HS_Elo(defaultK=K)

    #HCT German TakeTV (S1),Global Qualifier,1,Sintolol,Radogask,3,1
    #event,sub_event,
    filename = 'challenger_results.csv'
    rating = {}
    rating_games = {}
    wins = {}
    expected = []
    errors = []
    baseline = []
    bucket_pred = {}
    bucket_res = {}
    file = open(filename)
    lines = [line for line in file]
    lines.sort(key=lambda x:x[3])
    for line in lines:
        event, date, round_num, p1, p2, score1, score2 = line.strip().split(',')
        if score1 == 'None' or score2 == 'None': 
            continue
        score1 = int(score1)
        score2 = int(score2)
        round_num = int(round_num)
        p1 = p1.lower()
        p2 = p2.lower()
        if max(score1, score2) != 2: continue
        if score1 == score2: continue
        result = score1 > score2
        rating_games[p1] = rating_games.get(p1, 0) + 1
        rating_games[p2] = rating_games.get(p2, 0) + 1
        if p1 not in rating:
            rating[p1] = env.create_rating()
        if p2 not in rating:
            rating[p2] = env.create_rating()
        #print(env.quality_1vs1(rating[p1], rating[p2]))
        est = env.expect_score(rating[p1], rating[p2])
        if min(rating_games[p1], rating_games[p2]) >= 10:
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
    file.close()

    min_games = 0

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
        #print(K, round(sum(errors) / len(errors), 5))

        
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
