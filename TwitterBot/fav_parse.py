import json
import datetime
from stream_listener import TwitterListener
import time

import sys
sys.path.append('../')
from config import basedir
sys.path.append(basedir)
sys.path.append(basedir + '/lineupSolver')

import re
deckstring_re = re.compile('(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{4}){12,}')

import tweepy
from twitter_config import *
from deck_manager import *

listener = TwitterListener()
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)
me = api.me()
#stream = tweepy.Stream(auth, listener, tweet_mode='extended')

likes = []
for i in range(0, 10):
    print(i)
    tmp = [i.id for i in api.favorites(page=i)]
    if not tmp: break
    likes += tmp

all_decks = []
for post_id in likes:
    i = api.get_status(post_id, tweet_mode='extended')
    #test_text = "".join(i.full_text.split('\n'))
    test_text = i.full_text
    deckstring_matches_tmp = deckstring_re.findall(test_text)
    deckstring_matches = []
    for ds in deckstring_matches_tmp:
        try:
            deck = EasyDeck(ds)
            deckstring_matches.append(ds)
        except:
            pass
    
    if deckstring_matches:
        #time = datetime.datetime.strptime(i.created_at[:19] + i.created_at[-5:], "%a %b %d %H:%M:%S %Y")
        time = i.created_at
        text_time = time.strftime("%Y_%m_%d %H:%M:%S")
        user = i.user.screen_name
        if text_time >= '2018_05_26':
            #res.append((text_time, user, deckstring_matches, test_text))
            #print('.', end='')
            #if i.id not in likes:
            print(text_time, user,deckstring_matches)
            print(test_text)
            print("id:", i.id)
            for d in deckstring_matches:
                try:
                    #EasyDeck(d).print_deck()
                    all_decks.append((text_time, user, EasyDeck(d)))
                except:
                    pass
            #api.create_favorite(i.id)
            #print("###")
            #logfile.write("%-25s %s %s\n" % (user, text_time, deckstring_matches))

for date, user, deck in sorted(all_decks, key=lambda x:x[0]):
    print(user, date)
    deck.print_deck()
