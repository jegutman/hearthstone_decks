#from backports import csv
from hearthstone.deckstrings import Deck
from hearthstone.deckstrings import FormatType
import json
# Python3 version https://pillow.readthedocs.io
import io
import os
import argparse
import re
import requests
from html.parser import HTMLParser
from pprint import pprint

deckstring_re = re.compile('(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{4}){12,}')

def psearch(player_search):
    res = [i for i in matches if i[0].lower().startswith(player_search.lower()) or i[1].lower().startswith(player_search.lower())]
    pprint(res)

def write_to_csv(deck_dict, code_dest):
    with open(code_dest, 'w') as f:
        for name in deck_dict:
            f.write('{},{}\n'.format(name, ','.join(deck_dict[name])))

def parse_deck(text):
    for i in range(3):
        try:
            deck = Deck.from_deckstring(text+'='*i)
            return deck
        except Exception as e:
            continue
    return None

def decks_from_battlefy(battlefy_url, dest, ordered=False, code_dest=None):
    if ordered:
        setup_dirs(dest)
    deck_dict = {}
    valid = re.compile(r"^(?:https://)?\/?battlefy.com\/([^:/\s]+)/([^:\/\s]+)/([\w\d]+)/stage/([\w\d]+)/bracket/(\d*)$")
    bracketf= 'https://dtmwra1jsgyb0.cloudfront.net/stages/{}/matches'
    matchf = 'https://dtmwra1jsgyb0.cloudfront.net/matches/{}?extend%5Btop.team%5D%5Bplayers%5D%5Buser%5D=true&extend%5Bbottom.team%5D%5Bplayers%5D%5Buser%5D=true'
    matches = valid.match(battlefy_url)
    if matches is None:
        print("Unable to parse battlefy url. Please get the bracket from the brackets tab")
        return
    groups = matches.groups()
    org = groups[0]
    event = groups[1]
    eventcode = groups[2]
    stagecode = groups[3]
    roundNum = groups[4]
    bracket_url = bracketf.format(stagecode)
    data = json.loads(requests.get(bracket_url).text)
    deck_dict = {}

    return data
    for x in data:
        # Check if we need to make an http request by checking if we already have this person's decks
        if not any(['team' in x[i] and x[i]['team']['name'] not in deck_dict for i in ['top', 'bottom']]):
            continue
        r = requests.get(matchf.format(x['_id']))
        matchdata = json.loads(r.text)
        for i in ['top', 'bottom']:
            team = matchdata[0][i]
            if 'team' not in team or team['team']['name'] in deck_dict:
                continue
            name = team['team']['name']
            decks = team['team']['players'][0]['gameAttributes']['deckStrings']
            deck_dict[name] = []
            for decklist in decks:
                deck = parse_deck(decklist)
                if deck!=None:
                    deck_dict[name].append(deck.as_deckstring)
    if code_dest:
        write_to_csv(deck_dict, code_dest)
    else:
        generate_images(deck_dict, dest, ordered)

"""
NOTES ON battlefy parsing
get names game['top']['team']['name']
get deck codes game['top']['customFields']  (mabye [-4:])
'bannedClass'
'winner'
games in  game['stats']
    ['top']['class']
    ['top']['winner']
"""
def parse_match(match):
    if 'isComplete' not in match.keys():
        return None
    elif match['isBye']:
        return None
    p1 = match['top']['team']['name']
    p2 = match['bottom']['team']['name']

    if 'seedNumber' in match['top']:
        p1_seed = match['top']['seedNumber']
    else:
        p1_seed = -1
    if 'seedNumber' in match['bottom']:
        p2_seed = match['bottom']['seedNumber']
    else:
        p2_seed = -1

    p1_decks = []
    for field in match['top']['team']['customFields']:
        deck_match = deckstring_re.findall(field['value'])
        if deck_match:
            p1_decks.append(deck_match[0])
    p2_decks = []
    for field in match['bottom']['team']['customFields']:
        deck_match = deckstring_re.findall(field['value'])
        if deck_match:
            p2_decks.append(deck_match[0])

    if 'bannedClass' in match['top']:
        p1_banned = match['top']['bannedClass']
    else:
        p1_banned = ''
    if 'bannedClass' in match['bottom']:
        p2_banned = match['bottom']['bannedClass']
    else:
        p2_banned = ''
    

    result = 1 if match['top']['winner'] else 0
    
    games = []
    if 'stats' in match.keys():
        for game in match['stats']:
            p1_tmp_class = game['stats']['top']['class']
            p2_tmp_class = game['stats']['bottom']['class']
            tmp_result = 1 if game['stats']['top']['winner'] else 0
            games.append((p1_tmp_class, p2_tmp_class, tmp_result))

    p1_score = match['top']['score']
    p2_score = match['bottom']['score']
    
    return (p1, p2, result, p1_score, p2_score, p1_seed, p2_seed, p1_decks, p2_decks, games)
        
#bracket_url = 'https://battlefy.com/hearthstone-esports/2018-hct-asia-pacific-summer-playoffs/5acfd7384f598e034a21c245/stage/5aff76a9a22b3a03b613041f/bracket/'
bracket_url = 'https://battlefy.com/esl-brasil/hearthstone-copa-america-summer-season-global-qualifier/5a4e71173b5ae7038a45d8b4/stage/5a57b4d5f3eae5035dee3642/bracket/'
data = decks_from_battlefy(bracket_url, 'decks.csv',ordered=False,code_dest='decks.csv')

matches = []
failed = []
seeds = {}
count = 0
for i in data:
    count += 1
    print(count)
    match = parse_match(i)
    if not match:
        print('failed')
        
    #try:
    #    p1 = i['top']['team']['name']
    #    p2 = i['bottom']['team']['name']
    #    try:
    #        seeds[i['top']['seedNumber']] = p1
    #        seeds[i['bottom']['seedNumber']] = p1
    #    except:
    #        pass
    #    result = 'W' if i['top']['winner'] else 'L'
    #except:
    #    failed.append(i)
    #    continue
    #matches.append((p1,p2,result))
