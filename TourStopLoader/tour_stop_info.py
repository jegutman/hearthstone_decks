from battlefy_decks_results import *
from smash_decks_results import *

filename = 'tour_stop_info.csv'
tourstops = open(filename)
count = 0
for line in tourstops:
    count += 1
    #if count % 6 != 0: continue
    line = line.strip()
    tmp = line.split(',')
    print(tmp)
    event, sub_event, event_format, sub_bracket, bracket_url = tmp
    if not bracket_url: continue
    if 'battlefy' in bracket_url:
        process_battlefy_url(bracket_url)
    elif 'battlefy' not in bracket_url:
        tournament_name = bracket_url
        print(tournament_name)
        parse_smash_tournament(tournament_name)
