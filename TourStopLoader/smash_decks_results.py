#from backports import csv
from datetime import datetime
from hearthstone.deckstrings import Deck
from hearthstone.deckstrings import FormatType
import json
import io
import os
import argparse
import re
import requests
from html.parser import HTMLParser
from pprint import pprint
import pycookiecheat
from fake_useragent import UserAgent

ua = UserAgent()

deckstring_re = re.compile('(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{4}){12,}')

class SmashHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.extracted = ''

    def handle_data(self, data):
        if data.strip().startswith("window.bootstrappedData="):
            self.extracted = data.strip()[len('window.bootstrappedData='):-1]

def search(x, y):
    for i,j in x.items():
        if y in str(j):
            print(i)

smashgg_hero_map = {
    617 : 'Paladin',
    618 : 'Druid',
    619 : 'Hunter',
    620 : 'Mage',
    621 : 'Priest',
    622 : 'Rogue',
    623 : 'Shaman',
    624 : 'Warlock',
    625 : 'Warrior',
}

def decks_from_smashgg(bracket_url, entrants):
    test_entrants = entrants
    deck_dict = {}
    header = {'User-Agent':str(ua.chrome)}
    url_base = 'https://smash.gg/'
    cookies = pycookiecheat.chrome_cookies(url_base)
    html = requests.get(bracket_url, cookies = cookies, headers=header).text
    #html = requests.get(bracket_url).text
    parser = SmashHTMLParser()
    parser.feed(html)
    data = json.loads(parser.extracted)['dehydratedState']['context']['dispatcher']['stores']
    hero_map = {617:671, 618:274, 619:31, 620:637, 621:813, 622:930,
            623:1066, 624:893, 625:7}
    reverse_map = {}
    for _, card in data['CardStore']['card'].items():
        reverse_map[int(card['id'])] = int(card['externalId'])
    for _, deck in data['CardDeckStore']['cardDeck'].items():
        #name = data['EntrantStore']['entrants'][str(deck['entrantId'])]['name']
        #name = entrants.get(deck['entrantId'], deck['entrantId'])
        name = entrants[deck['entrantId']]
        cards = {}
        for card in deck['cardIds']:
            if card not in cards:
                cards[card] = 0
            cards[card]+=1
        hero = hero_map[deck['characterIds'][0]]
        deck = Deck()
        deck.heroes = [hero]
        deck.format = FormatType.FT_STANDARD
        deck.cards = [(reverse_map[x], cards[x]) for x in cards]
        if name not in deck_dict:
            deck_dict[name] = []
        deck_dict[name].append(deck.as_deckstring)
    return deck_dict

bracket_url = 'https://smash.gg/tournament/dreamhack-hct-grand-prix-tours-2018/events/dreamhack-hct-hearthstone-grand-prix-tours-2018/brackets/239288'
#bracket_url = "https://smash.gg/tournament/dreamhack-hct-grand-prix-tours-2018/events/dreamhack-hct-hearthstone-grand-prix-tours-2018/set/15199801"

#### API Tournament
#### 'https://api.smash.gg/tournament/dreamhack-hct-grand-prix-tours-2018?expand[]=phase&expand[]=groups&expand[]=event

def parse_smash_tournament(tournament_name):
    decks = {}
    matches = []
    tournament_url = 'https://api.smash.gg/tournament/%(tournament_name)s?expand[]=phase&expand[]=groups&expand[]=event'
    bracket_url = 'https://api.smash.gg/phase_group/%(bracket_id)s?expand[]=entrants&expand[]=sets'
    tournament_data = json.loads(requests.get(tournament_url % locals()).text)
    phase_map = {}
    player_matches = {}
    url_slug = 'https://smash.gg/' + tournament_data['entities']['event'][0]['slug'].replace('event', 'events') + '/brackets/%(phase_id)s'
    for phase_data in tournament_data['entities']['phase']:
        phase_map[phase_data['id']] = phase_data['name']
    for bracket in tournament_data['entities']['groups']:
        entrants = {}
        bracket_id = bracket['id']
        phase_id = bracket['phaseId']
        #print(url_slug % locals())
        bracket_name = phase_map[bracket['phaseId']]
        bracket_data = json.loads(requests.get(bracket_url % locals()).text)
        for entrant_data in bracket_data['entities']['entrants']:
            entrants[entrant_data['id']] = tuple(entrant_data['mutations']['players'].values())[0]['gamerTag'].split('#')[0].strip()
        decks.update(decks_from_smashgg(url_slug % locals(), entrants))
        #for i in sorted(entrants.values()):
        #    print(i)
        for set_data in bracket_data['entities']['sets']:
            p1_id = set_data['entrant1Id']
            p2_id = set_data['entrant2Id']
            if not p1_id or not p2_id: continue
            p1 = entrants[p1_id]
            p2 = entrants[p2_id]
            p1_score = set_data['entrant1Score']
            p2_score = set_data['entrant2Score']
            game_time = set_data['completedAt']
            #game_time = datetime.fromtimestamp(set_data['completedAt'])
            #date = game_time.strftime("%Y_%m_%d %H:%M:%S")
            round_num = set_data['round']
            games = []
            match_res = (game_time, bracket_name, round_num, p1, p2, p1_score, p2_score, games)
            matches.append(match_res)
            #print(match_res)
    return decks, matches, player_matches

            # entrant1Id, entrant2Id, entrant1Score,entrant2Score, date

#decks = decks_from_smashgg('https://smash.gg/tournament/dreamhack-hct-grand-prix-tours-2018/event/dreamhack-hct-hearthstone-grand-prix-tours-2018/brackets/239288')
#decks, matches = parse_smash_tournament('dreamhack-hct-grand-prix-tours-2018')
#decks = decks_from_smashgg('https://smash.gg/tournament/dreamhack-hct-grand-prix-tours-2018/event/dreamhack-hct-hearthstone-grand-prix-tours-2018')
#decks = decks_from_smashgg('https://smash.gg/tournament/dreamhack-hct-grand-prix-tours-2018/events/dreamhack-hct-hearthstone-grand-prix-tours-2018/brackets/239288')
#decks = decks_from_smashgg('https://smash.gg/tournament/dreamhack-hct-grand-prix-tours-2018/event/dreamhack-hct-hearthstone-grand-prix-tours-2018/brackets/239288')

#decks, matches = parse_smash_tournament('dreamhack-hct-grand-prix-austin-2018')
#decks, matches = parse_smash_tournament('hct-toronto-at-eglx-2018-1')
