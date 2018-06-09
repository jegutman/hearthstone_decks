import requests
from datetime import * 
import time
import sys
import MySQLdb
sys.path.append('../')
from config import basedir
sys.path.append(basedir)
sys.path.append(basedir + '/lineupSolver')
from json_cards_to_python import *
from deck_manager import *
from hearthstone import *
import random
from label_archetype

def convert(cards):
    res = {}
    for card in cards:
        if card[-2] == 't':
            card = card[:-2]
        if card[-1] == 't':
            card = card[:-1]
        dbfId = card_id_to_dbfId[card]
        res[dbfId] = res.get(dbfId,0) + 1
    cards = [(i,j) for i,j in res.items()]
    return cards

name_counter = 0
def unknown_name(name):
    global name_counter
    global name_overrides
    name_counter = random.randint(1, 999)
    res_name = "unknownuser%s" % name_counter
    name_overrides[name] = res_name
    print("NAME_OVERRIDES", name_overrides)
    return res_name


name_overrides = {
    'ШтанУдачи' : 'ShtanUdachi',
}

url = "https://hsreplay.net/api/v1/live/replay_feed/?format=json&offset=%(offset)s"
game_url = "https://hsreplay.net/api/v1/games/%(game_id)s/?format=json"

connection = MySQLdb.connect(host='localhost', user=db_user, passwd=db_passwd)
#connection.set_character_set('utf8')
cursor = connection.cursor()
#cursor.execute('SET NAMES utf8;')
#cursor.execute('SET CHARACTER SET utf8;')
#cursor.execute('SET character_set_connection=utf8;')

archetypes_url = 'https://hsreplay.net/api/v1/archetypes/?format=json'
archetypes_json = requests.get(archetypes_url).json()

archetype_names = {}
archetype_ids = {}
for archetype in archetypes_json:
    archetype_names[archetype['id']] = archetype['name']
    archetype_ids[archetype['name']] = archetype['id']

def get_archetype(arch_id):
    res = archetype_names.get(int(arch_id))
    return res

games = []
#max_game = 200
offset = 0
game_ids = []
count = 0
game_count = 0
while True:
    count += 1
    print("COUNT :", count)
    try:
        tmp_games = requests.get(url % locals()).json()['data']
    except:
        print("Failed to connect")
        time.sleep(60)
        continue
    for game in tmp_games:
        game_id      = game['id']

        if game_id in game_ids: continue
        game_ids.append(game_id)

        p1_rank      = game['player1_rank']
        p2_rank      = game['player2_rank']
        p1_l_rank    = game['player1_legend_rank']
        p2_l_rank    = game['player2_legend_rank']

        p1_won       = game['player1_won']
        p2_won       = game['player2_won']
        archetype1   = get_archetype(game['player1_archetype'])
        archetype2   = get_archetype(game['player2_archetype'])
        p1_rank = int(p1_rank) if p1_rank != 'None' else 0
        p2_rank = int(p2_rank) if p2_rank != 'None' else 0
        if p1_rank <= 5 or p2_rank <= 5:
            if p1_rank > 0:
                p1_insert_rank = p1_rank
            else:
                p1_insert_rank = 'L' + str(p1_l_rank)
            if p2_rank > 0:
                p2_insert_rank = p2_rank
            else:
                p2_insert_rank = 'L' + str(p2_l_rank)
            try:
            #if True:
                game_count += 1
                game_info = requests.get(game_url % locals()).json()
                time_info = game_info['global_game']['match_start']
                end_time_info = game_info['global_game']['match_end']

                game_time = datetime.strptime(time_info[:19], "%Y-%m-%dT%H:%M:%S").strftime("%s")
                end_time = datetime.strptime(end_time_info[:19], "%Y-%m-%dT%H:%M:%S").strftime("%s")
                game_date = time_info[:10].replace('-', '_')
                first = 1 if game_info['friendly_player']['is_first'] else 0
                result = 'W' if game_info['won'] else 'L'

                #game_infos[game_id] = game_info
                p1 = game_info['friendly_player']['name']
                    
                if p1 in name_overrides:
                    p1 = name_overrides[p1]
                else:
                    if (len(str(p1_insert_rank)) <= 4 and str(p1_insert_rank)[0] == 'L') or (len(str(p2_insert_rank)) <= 4 and str(p2_insert_rank)[0] == 'L'):
                        try:
                            p1.encode("iso-8859-1")
                        except:
                            p1 = unknown_name(p1)
                        
                
                p2 = game_info['opposing_player']['name']
                if p2 in name_overrides:
                    p2 = name_overrides[p2]
                else:
                    if (len(str(p1_insert_rank)) <= 4 and str(p1_insert_rank)[0] == 'L') or (len(str(p2_insert_rank)) <= 4 and str(p2_insert_rank)[0] == 'L'):
                        try:
                            p2.encode("iso-8859-1")
                        except:
                            p2 = unknown_name(p2)

                p1_deckstring = ''
                p2_deckstring = ''
                known_p1_deckstring = ''
                known_p2_deckstring = ''
                try:
                    friendly_cards = []
                    known_friendly_cards = []
                    if game_info['friendly_deck']['cards']: friendly_cards += game_info['friendly_deck']['cards']
                    if game_info['friendly_deck']['cards']: known_friendly_cards += game_info['friendly_deck']['cards']
                    if game_info['friendly_deck']['predicted_cards']: friendly_cards = game_info['friendly_deck']['predicted_cards']
                    friendly_heroes = [card_id_to_dbfId[game_info['friendly_player']['hero_id']]]
                    
                    friendly_deck = deckstrings.Deck()
                    friendly_deck.cards = convert(friendly_cards)
                    friendly_deck.heroes = friendly_heroes
                    friendly_deck.format = 2
                    friendly_deckstring = friendly_deck.as_deckstring
                    p1_deckstring = friendly_deckstring

                    known_friendly_deck = deckstrings.Deck()
                    known_friendly_deck.cards = convert(known_friendly_cards)
                    known_friendly_deck.heroes = friendly_heroes
                    known_friendly_deck.format = 2
                    known_friendly_deckstring = known_friendly_deck.as_deckstring
                    known_p1_deckstring = known_friendly_deckstring
                except:
                    p1_deckstring = ''
                    known_p1_deckstring = ''
                    
                try:
                    opposing_cards = []
                    known_opposing_cards = []
                    if game_info['opposing_deck']['cards']: opposing_cards += game_info['opposing_deck']['cards']
                    if game_info['opposing_deck']['cards']: known_opposing_cards += game_info['opposing_deck']['cards']
                    if game_info['opposing_deck']['predicted_cards']: opposing_cards = game_info['opposing_deck']['predicted_cards']
                    opposing_heroes = [card_id_to_dbfId[game_info['opposing_player']['hero_id']]]

                    opposing_deck = deckstrings.Deck()
                    opposing_deck.cards = convert(opposing_cards)
                    opposing_deck.heroes = opposing_heroes
                    opposing_deck.format = 2
                    opposing_deckstring = opposing_deck.as_deckstring
                    p2_deckstring = opposing_deckstring

                    known_opposing_deck = deckstrings.Deck()
                    known_opposing_deck.cards = convert(known_opposing_cards)
                    known_opposing_deck.heroes = opposing_heroes
                    known_opposing_deck.format = 2
                    known_opposing_deckstring = known_opposing_deck.as_deckstring
                    known_p2_deckstring = known_opposing_deckstring
                except:
                    p2_deckstring = ''
                    known_p2_deckstring = ''

                if game_info['friendly_player']['player_id'] != 1:
                    print("Swapped")
                    p1, p2 = p2, p1
                    result = 'L' if result == 'W' else 'W'
                    first = 1 - first
                    #friendly_deckstring, opposing_deckstring = opposing_deckstring, friendly_deckstring
                    p1_deckstring, p2_deckstring = p2_deckstring, p1_deckstring
                    known_p1_deckstring, known_p2_deckstring = known_p2_deckstring, known_p1_deckstring
                print(game_id, p1_deckstring, p2_deckstring)
                
                num_turns = game_info['global_game']['num_turns']
                ladder_season = game_info['global_game']['ladder_season']
                game_format = game_info['global_game']['format']
                archetype1 = archetype1.strip()
                archetype2 = archetype2.strip()
                try:
                    if p1_deckstring:
                        archetype1 = label_archetype(EasyDeck(p1_deckstring), old_archetype=archetype1)
                except Exception as e:
                    print(e)
                    pass
                try:
                    if p2_deckstring:
                        archetype2 = label_archetype(EasyDeck(p2_deckstring), old_archetype=archetype2)
                except Exception as e:
                    print(e)
                    pass
                cursor.execute("""INSERT INTO hsreplay.hsreplay (game_id, time, date, p1, p2, archetype1, archetype2, p1_rank, p2_rank, num_turns, ladder_season, format, first, result, processed)
                                  VALUES ('%(game_id)s', %(end_time)s, '%(game_date)s', '%(p1)s', '%(p2)s', '%(archetype1)s', '%(archetype2)s', '%(p1_insert_rank)s', '%(p2_insert_rank)s', %(num_turns)s, 
                                           %(ladder_season)s, %(game_format)s, %(first)s, '%(result)s', 0)""" % locals())
                cursor.execute("""INSERT INTO hsreplay.hsreplay_decks (game_id, p1_deck_code, p2_deck_code, known_p1_deck_code, known_p2_deck_code) 
                                  VALUES ('%(game_id)s', '%(p1_deckstring)s', '%(p2_deckstring)s', '%(known_p1_deckstring)s', '%(known_p2_deckstring)s')""" % locals())
                connection.commit()
                #time_string = datetime.now().strftime("%Y_%m_%d %H:%M:%S")
                time_string = datetime.strptime(time_info[:19], "%Y-%m-%dT%H:%M:%S").strftime("%Y_%m_%d %H:%M:%S")
                print("%(time_string)s INSERTED: %(p1)-25s %(p2)-25s %(result)s %(archetype1)-25s %(archetype2)-25s %(p1_insert_rank)-10s %(p2_insert_rank)-10s" % locals())
            except Exception as e:
                try:
                    #time_string = datetime.now().strftime("%Y_%m_%d %H:%M:%S")
                    time_string = datetime.strptime(time_info[:19], "%Y-%m-%dT%H:%M:%S").strftime("%Y_%m_%d %H:%M:%S")
                    print("%(time_string)s FAILED: %(p1)-25s %(p2)-25s %(result)s %(archetype1)-25s %(archetype2)-25s %(p1_insert_rank)-10s %(p2_insert_rank)-10s" % locals())
                except:
                    pass
                print("SOMETHING FAILED")
                print(e)
                continue
    time.sleep(5)

#counts = {}
#for i,j,k in games:
#    counts[i] = counts.get(i, 0) + 1
#    counts[j] = counts.get(j, 0) + 1
#for i, j in sorted(counts.items(), key=lambda x:x[1], reverse=True):
#    print(j, i)

