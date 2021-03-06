import sys
sys.path.append('../')
from config import basedir
sys.path.append(basedir)
sys.path.append(basedir + '/lineupSolver')
#from backports import csv
from hearthstone.deckstrings import Deck
from hearthstone.deckstrings import FormatType
import json
from deck_manager import *
import re
import requests
from html.parser import HTMLParser

deckstring_re = re.compile('(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{4}){12,}')

def print_player(player):
    for i in player_matches[player]:
        print(i[2], i[3], i[5], i[6])
        for j in i[-1]:
            print('    ',j)


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

player_decks = {}
seeds = {}

def matches_from_battlefy(battlefy_url, dest, ordered=False, code_dest=None):
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
    global player_decks, seeds
    matchf = 'https://dtmwra1jsgyb0.cloudfront.net/matches/{}?extend%5Btop.team%5D%5Bplayers%5D%5Buser%5D=true&extend%5Bbottom.team%5D%5Bplayers%5D%5Buser%5D=true'
    if 'isComplete' not in match.keys():
        return None
    elif match['isBye']:
        return None
    if not match['top'] or not match['bottom']:
        return None
    if 'team' not in match['top']:
        return None
    if 'team' not in match['bottom']:
        return None
    date = match['updatedAt'][:10].replace('-', '_')
    round_number = match['roundNumber']
    p1 = match['top']['team']['name'].replace(' \#', '#').split(' ')[0].split('(')[0]
    p1 = p1.split('#')[0]
    if p1 not in player_decks: player_decks[p1] = []
    p2 = match['bottom']['team']['name'].replace(' #', '#').split(' ')[0].split('(')[0]
    p2 = p2.split('#')[0]
    if p2 not in player_decks: player_decks[p2] = []

    if 'seedNumber' in match['top']:
        seeds[p1] = match['top']['seedNumber']
    if 'seedNumber' in match['bottom']:
        seeds[p2] = match['bottom']['seedNumber']

    p1_decks = player_decks.get(p1, [])
    p2_decks = player_decks.get(p2, [])
    if not p1_decks or not p2_decks:
        try:
            if not p1_decks:
                for field in match['top']['team']['customFields']:
                    deck_match = deckstring_re.findall(field['value'])
                    if deck_match:
                        p1_decks.append(deck_match[0])
                player_decks[p1] = p1_decks
            if not p2_decks:
                for field in match['bottom']['team']['customFields']:
                    deck_match = deckstring_re.findall(field['value'])
                    if deck_match:
                        p2_decks.append(deck_match[0])
                player_decks[p2] = p2_decks
        except:
            r = requests.get(matchf.format(match['_id']))
            matchdata = json.loads(r.text)
            if not p1_decks:
                team = matchdata[0]['top']
                if 'team' in team:
                    decks = team['team']['players'][0]['gameAttributes']['deckStrings']
                    for decklist in decks:
                        deck = parse_deck(decklist)
                        if deck!=None:
                            p1_decks.append(deck.as_deckstring)
                player_decks[p1] = p1_decks
            if not p2_decks:
                team = matchdata[0]['bottom']
                if 'team' in team:
                    decks = team['team']['players'][0]['gameAttributes']['deckStrings']
                    for decklist in decks:
                        deck = parse_deck(decklist)
                        if deck!=None:
                            p2_decks.append(deck.as_deckstring)
                player_decks[p2] = p2_decks

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
    
    return (date, round_number, p1, p2, result, p1_score, p2_score, games)
        
#bracket_url = 'https://battlefy.com/hct-tokyo-tour-stop/hct-tokyo-tour-stop-global-open-qualifier-1-america-server/5acf16cb5afa0d034c3cfcf2/stage/5b2dabb7a11aa6039e8032a5/bracket/'
#bracket_url = 'https://battlefy.com/hct-tokyo-tour-stop/hct-tokyo-tour-stop-global-qualifier-2-america-server/5ad6fb258fbdcf0355517c35/stage/5b36e2299a4af103b49bff0d/bracket/'
#bracket_url = 'https://battlefy.com/blizzardzhtw/hct-tour-stop-taipei-global-open-qualifier-america-server/5aa883a4e20b840351ff2fa7/stage/5ac074da60cd4803480a2f79/bracket/'
#bracket_url = 'https://battlefy.com/hearthstone-esports/2018-hct-asia-pacific-summer-playoffs/5acfd7384f598e034a21c245/stage/5aff76a9a22b3a03b613041f/bracket/'
#bracket_url = 'https://battlefy.com/esl-brasil/hearthstone-copa-america-summer-season-global-qualifier/5a4e71173b5ae7038a45d8b4/stage/5a57b4d5f3eae5035dee3642/bracket/'
#bracket_url = 'https://battlefy.com/take-tv/hct-germany-a-taketv-tour-stop-global-qualifier/5b3507da2c185e0397195db8/stage/5b4382bdd4facf039b6922f5/bracket/'
bracket_url = 'https://battlefy.com/take-tv/hct-germany-a-taketv-tour-stop-global-qualifier/5b3507da2c185e0397195db8/stage/5b35088373abf503c89a2351/bracket/'
#bracket_urls = [
#    'https://battlefy.com/take-tv/hct-germany-a-taketv-tour-stop-global-qualifier/5b3507da2c185e0397195db8/stage/5b43836852891c03e07ea9ea/bracket/', 
#    'https://battlefy.com/take-tv/hct-germany-a-taketv-tour-stop-global-qualifier/5b3507da2c185e0397195db8/stage/5b35088373abf503c89a2351/bracket/',
#    'https://battlefy.com/take-tv/hct-germany-a-taketv-tour-stop-global-qualifier/5b3507da2c185e0397195db8/stage/5b4382bdd4facf039b6922f5/bracket/',
#    'https://battlefy.com/take-tv/hct-germany-a-taketv-tour-stop-global-qualifier/5b3507da2c185e0397195db8/stage/5b4383c4439a3803c73d7040/bracket/',
#    ]
#bracket_urls = [
#    'https://battlefy.com/evox/hct-tour-stop-italy-powered-by-zotac/5aa7d09f0b25e50393914521/stage/5aa7d0ba0f99cf034ea52f06/bracket/9',
#]
bracket_urls = [
    'https://battlefy.com/take-tv/hct-germany-a-taketv-tour-stop-european-qualifier-1/5b350c75b36e6203a5e2eb02/stage/5b45420e13c25703b3834359/bracket/',
    'https://battlefy.com/take-tv/hct-germany-a-taketv-tour-stop-european-qualifier-1/5b350c75b36e6203a5e2eb02/stage/5b454207b394d103b9bad75a/bracket/',
    'https://battlefy.com/take-tv/hct-germany-a-taketv-tour-stop-european-qualifier-1/5b350c75b36e6203a5e2eb02/stage/5b45422ae2eb9603ba9a99da/bracket/',
    'https://battlefy.com/take-tv/hct-germany-a-taketv-tour-stop-european-qualifier-1/5b350c75b36e6203a5e2eb02/stage/5b4542678c67fb03e0534cb5/bracket/',
    ]
matches = []
failed = []
count = 0
player_matches = {}
for bracket_url in bracket_urls:
    data = matches_from_battlefy(bracket_url, 'decks.csv',ordered=False,code_dest='decks.csv')

    for i in data:
        count += 1
        print(count)
        match = parse_match(i)
        if not match:
            print('failed')
            failed.append(i)
        else:
            matches.append(match)
            p1, p2 = match[2], match[3]
            p1 = p1.split('#')[0].strip()
            p2 = p2.split('#')[0].strip()
            player_matches[p1] = player_matches.get(p1, []) + [match]
            player_matches[p2] = player_matches.get(p2, []) + [match]
            
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
wins = {}
losses = {}
for x in player_matches.keys():
    total_losses = sum([1-i[4] if i[2] == x else i[4] for i in player_matches[x]])
    total_wins = sum([i[4] if i[2] == x else 1-i[4] for i in player_matches[x]])
    wins[x] = total_wins
    losses[x] = total_losses
    if total_losses == 0 and total_wins >5:
        print(x)

