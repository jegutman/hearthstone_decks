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

paid_tournaments = [
    ('HCT Austin', 'Dreamhack Austin'),
    ('HCT Bangkok', 'HCT Bangkok'),
    ('HCT Italy', 'HCT Italy'),
    ('HCT Montreal', 'Dreamhack Montreal'),
    ('HCT Oakland', 'Esports Arena Oakland'),
    ('HCT Oslo', 'HCT Oslo'),
    ('HCT Seoul', 'HCT Seoul'),
    ('HCT Summer', 'Dreamhack Jonkoping'),
    ('HCT Taichung', ''),
    ('HCT Toronto (EGLX)', 'HCT Toronto'),
    ('HCT Tours', 'HCT Tours'),
    ('HCT Oslo (S3)', 'HCT Oslo (S3)'),
    ('HCT Singapore', 'HCT Singapore'),
    ('HCT Orange County', 'HCT Orange County'),
    ('HCT Atlanta', 'Dreamhack Atlanta'),
]

def logloss(result, predicted, eps=1e-15):
    if result == 1:
        return -math.log(predicted)
    else:
        return -math.log(1 - predicted)

tournament_sets = {}

filename = basedir + '/TourStopLoader/hct_results.csv'
file = open(filename)
lines = [line.strip().split(',') for line in file]
for line in lines:
    if line[3][:2] != '20':
        line[3] = datetime.datetime.fromtimestamp(int(line[3])).strftime("%Y_%m_%d")
        
#lines.sort(key=lambda x:x[3])
for line in sorted(lines, key=lambda x:(x[3], x[5])):
    #event, sub_event, sub_bracket, date, season, patch, round_num, p1, p2, score1, score2 = line.strip().split(',')
    event, sub_event, sub_bracket, date, season, patch, round_num, p1, p2, score1, score2 = line
    #print(date)
    #if date < '2018_07_01': continue
    tournament = (event, sub_event)
    #tournaments.add(tournament)
    # EXCLUDE ONLINE
    #if tournament not in offline_tournaments: continue
    if tournament not in paid_tournaments: continue
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
    if p1 not in tournament_sets:
        tournament_sets[p1] = set()
    if p2 not in tournament_sets:
        tournament_sets[p2] = set()
    tournament_sets[p1].add(event)
    tournament_sets[p2].add(event)

#for i,j in sorted(tournament_sets.items(), key=lambda x:len(x[1]), reverse=True)[:150]:
for i,j in sorted(tournament_sets.items(), key=lambda x:len(x[1]), reverse=True):
    if len(j) < 3: break
    #print("%-20s %s" % (i, len(j)))
    print("%s,%s,%s" % (i, len(j), ",".join(sorted(list(j)))))
