from battlefy_decks_results import *
from smash_decks_results import *

filename = 'challenger_cups.csv'
tourstops = open(filename)
count = 0
result_out = open('challenger_results.csv', 'w')
decks_out = open('challenger_decks.csv', 'w')

for line in tourstops:
    count += 1
    #if count % 6 != 0: continue
    line = line.strip()
    tmp = line.split(',')
    #print(tmp)
    bracket_url = tmp[0]
    event = bracket_url.split('/')[4]
    tmp_decks, tmp_matches, tmp_player_matches = process_battlefy_url(bracket_url)
    print(len(tmp_matches))
    for date, round_number, p1, p2, result, p1_score, p2_score, games in sorted(tmp_matches, key=lambda x:(x[0], x[1])):
        p1, p2 = p1.lower(), p2.lower()
        res = [event, date, round_number, p1, p2, p1_score, p2_score]
        result_out.write(",".join([str(i) for i in res]))
        result_out.write("\n")
        #print(",".join([str(i) for i in res]))
    for player, lists in tmp_decks.items():
        res = [event, player] + lists
        decks_out.write(",".join([str(i) for i in res]))
        decks_out.write("\n")
