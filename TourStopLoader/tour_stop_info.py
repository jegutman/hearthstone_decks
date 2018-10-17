from battlefy_decks_results import *
from smash_decks_results import *

filename = 'tour_stop_info.csv'
tourstops = open(filename)
count = 0
result_out = open('hct_results.csv', 'w+')
decks_out = open('hct_decks.csv', 'w+')

non_parse_file = open('non_parse_events.csv')
non_parse_matches = {}
#APAC Playoffs,Top8,Conquest,2018_05_20,kin0531,bloodtrail,3,0
for line in non_parse_file:
    event, sub_event, event_format, date, p1, p2, score1, score2 = line.strip().split(',')
    if (event, sub_event) not in non_parse_matches:
        non_parse_matches[(event, sub_event)] = []
    #result = 1 if int(score1) > int(score2) else 0
    non_parse_matches[(event, sub_event)].append([event, sub_event, event_format, date, p1, p2, score1, score2])
    pass

print(non_parse_matches.keys())

for line in tourstops:
    count += 1
    #if count % 6 != 0: continue
    line = line.strip()
    tmp = line.split(',')
    #print(tmp)
    event, sub_event, event_format, sub_bracket, season, patch, bracket_url = tmp
    print("Loading: %s" % event)
    if bracket_url:
        if 'battlefy' in bracket_url:
            tmp_decks, tmp_matches, tmp_player_matches = process_battlefy_url(bracket_url)
        elif 'battlefy' not in bracket_url:
            tournament_name = bracket_url
            tmp_decks, tmp_matches, tmp_player_matches = parse_smash_tournament(tournament_name)
    if not bracket_url:
        if (event, sub_event) not in non_parse_matches: continue   
        for event, sub_event, event_format, date, p1, p2, p1_score, p2_score in non_parse_matches[(event, sub_event)]:
            p1, p2 = p1.lower(), p2.lower()
            res = [event, sub_event, '', date, season, patch, 0, p1, p2, p1_score, p2_score]
            result_out.write(",".join([str(i) for i in res]))
            result_out.write("\n")
    elif 'battlefy' in bracket_url:
        for date, round_number, p1, p2, result, p1_score, p2_score, games in sorted(tmp_matches, key=lambda x:(x[0], x[1])):
            if p1_score == 0 and p2_score == 0: continue
            p1, p2 = p1.lower(), p2.lower()
            res = [event, sub_event, sub_bracket, date, season, patch, round_number, p1, p2, p1_score, p2_score]
            result_out.write(",".join([str(i) for i in res]))
            result_out.write("\n")
            #print(",".join([str(i) for i in res]))
    else:
        #for date, round_number, p1, p2, result, p1_score, p2_score, games in sorted(tmp_matches, key=lambda x:(x[0], x[1])):
        for date, bracket_name, round_number, p1, p2, result, p1_score, p2_score, games in sorted(tmp_matches, key=lambda x:(x[0], x[2])):
            if p1_score == 0 and p2_score == 0: continue
            p1, p2 = p1.lower(), p2.lower()
            sub_bracket = bracket_name
            res = [event, sub_event, sub_bracket, date, season, patch, round_number, p1, p2, p1_score, p2_score]
            result_out.write(",".join([str(i) for i in res]))
            result_out.write("\n")
            #print(",".join([str(i) for i in res]))
    for player, lists in tmp_decks.items():
        player = player.lower()
        res = [event, sub_event, event_format, sub_bracket, season, patch, player] + lists
        decks_out.write(",".join([str(i) for i in res]))
        decks_out.write("\n")
