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

connection = MySQLdb.connect(host='localhost', user=db_user, passwd=db_passwd)
cursor = connection.cursor()
count = 0

cursor.execute("SELECT game_id, p1_deck_code, p2_deck_code FROM hsreplay.hsreplay_decks")
rows = [i for i in cursor.fetchall()]

count = 0
for game_id, d1, d2 in rows:
    try:
        EasyDeck(d1)
    except:
        "Failed: %s %s" %(game_id, d1)
    try:
        EasyDeck(d2)
    except:
        "Failed: %s %s" %(game_id, d2)
