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
    ('Copa America Fall', 'Live Finals'),
    ('Copa America Summer', 'Live Finals'),
    ('HCT Austin', 'Dreamhack Austin'),
    ('HCT Bangkok', 'HCT Bangkok'),
    ('HCT Germany TakeTV (S1)', 'Live Finals'),
    ('HCT Germany TakeTV (S3)', 'Live Finals'),
    ('HCT Italy', 'HCT Italy'),
    ('HCT Montreal', 'Dreamhack Montreal'),
    ('HCT Oakland', 'Esports Arena Oakland'),
    ('HCT Oslo', 'HCT Oslo'),
    ('HCT Season 1 Champs', 'Season 1 Championship'),
    ('HCT Seoul', 'HCT Seoul'),
    ('HCT Summer', 'Dreamhack Jonkoping'),
    ('HCT Sydney', 'Live Finals'),
    ('HCT Taichung', ''),
    ('HCT Taipei', 'Live Finals'),
    ('HCT Tokyo', 'Live Finals'),
    ('HCT Toronto (EGLX)', 'HCT Toronto'),
    ('HCT Tours', 'HCT Tours'),
    ('NA Playoffs', 'NA Playoffs'),
    ('EU Playoffs', 'EU Playoffs'),
    ('APAC Playoffs', 'APAC Playoffs'),
    ('HCT Oslo (S3)', 'HCT Oslo (S3)'),
    ('HCT Singapore', 'HCT Singapore'),
    ('HCT Season 2 Champs', 'Season 2 Championship'),
    ('HCT Orange County', 'HCT Orange County'),
    ('HCT Atlanta', 'Dreamhack Atlanta'),
]

def logloss(result, predicted, eps=1e-15):
    if result == 1:
        return -math.log(predicted)
    else:
        return -math.log(1 - predicted)

#for K in range(16, 64, 4):
tournaments = set()
for K in range(36, 38, 2):
    env = HS_Elo(defaultK=K)

    #HCT German TakeTV (S1),Global Qualifier,1,Sintolol,Radogask,3,1
    #event,sub_event,
    filename = basedir + '/TourStopLoader/hct_results.csv'
    rating = {}
    rating_games = {}
    wins = {}
    expected = []
    errors = []
    baseline = []
    bucket_pred = {}
    bucket_res = {}
    file = open(filename)
    lines = [line.strip().split(',') for line in file]
    for line in lines:
        if line[3][:2] != '20':
            line[3] = datetime.datetime.fromtimestamp(int(line[3])).strftime("%Y_%m_%d")
            
    lines.sort(key=lambda x:x[3])
    for line in sorted(lines, key=lambda x:(x[3], x[5])):
        #event, sub_event, sub_bracket, date, season, patch, round_num, p1, p2, score1, score2 = line.strip().split(',')
        event, sub_event, sub_bracket, date, season, patch, round_num, p1, p2, score1, score2 = line
        #print(date)
        #if date < '2018_07_01': continue
        tournament = (event, sub_event)
        tournaments.add(tournament)
        # EXCLUDE ONLINE
        if tournament not in offline_tournaments: continue
        #if int(season) != 3: continue
        if score1 == 'None' or score2 == 'None': 
            continue
        score1 = int(score1)
        score2 = int(score2)
        round_num = int(round_num)
        p1 = p1.lower()
        p2 = p2.lower()
        if max(score1, score2) != 3: continue
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
    file.close()

    def expose(r):
        return int(r.mu)

###

if __name__ == '__main__':
    fields = {}
    file = open(filename)
    lines = [line.strip().split(',') for line in file]
    for line in lines:
        if line[3][:2] != '20':
            line[3] = datetime.datetime.fromtimestamp(int(line[3])).strftime("%Y_%m_%d")
            
    lines.sort(key=lambda x:x[3])
    for line in sorted(lines, key=lambda x:(x[3], x[5])):
        #event, sub_event, sub_bracket, date, season, patch, round_num, p1, p2, score1, score2 = line.strip().split(',')
        event, sub_event, sub_bracket, date, season, patch, round_num, p1, p2, score1, score2 = line
        if p1 not in fields: fields[p1] = {}
        if p2 not in fields: fields[p2] = {}
        if (event, sub_event) not in fields[p1]: fields[p1][(event, sub_event)] = []
        if (event, sub_event) not in fields[p2]: fields[p2][(event, sub_event)] = []
        #print(date)
        #if date < '2018_07_01': continue
        tournament = (event, sub_event)
        tournaments.add(tournament)
        # EXCLUDE ONLINE
        if tournament not in offline_tournaments: continue
        #if int(season) != 3: continue
        if score1 == 'None' or score2 == 'None': 
            continue
        score1 = int(score1)
        score2 = int(score2)
        round_num = int(round_num)
        p1 = p1.lower()
        p2 = p2.lower()
        if max(score1, score2) != 3: continue
        if score1 == score2: continue
        fields[p1][(event, sub_event)].append(rating[p2].mu)
        fields[p2][(event, sub_event)].append(rating[p1].mu)
    file.close()

best_fields = []
for p in fields:
    for event in fields[p]:
        if len(fields[p][event]) <= 6: continue
        if 'Playoffs' in event[0]: continue
        #avg = int(sum(fields[p][event]) / len(fields[p][event]))
        avg = int(min(sorted(fields[p][event])[-6:]))
        best_fields.append((avg, p, event))

for i,j,k in sorted(best_fields, reverse=True)[:50]:
    print(j,i,k)
