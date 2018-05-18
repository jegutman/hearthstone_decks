import json
import datetime
from stream_listener import TwitterListener

import re
deckstring_re = re.compile('(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{4}){12,}')

import re

# Import the necessary methods from "twitter" library
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream
import tweepy
from twitter_config import *

listener = TwitterListener()
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)
stream = tweepy.Stream(auth, listener, tweet_mode='extended')


logfile = open('output.txt', 'w')

for i in stream.userstream():
    deckstring_matches = deckstring_re.findall(i['full_text'])
    if deckstring_matches:
        time = datetime.datetime.strptime(i['created_at'][:19] + i['created_at'][-5:], "%a %b %d %H:%M:%S %Y")
        text_time = time.strftime("%Y_%m_%d")
        if text_time > '2018_04_11':
            print(user, text_time, deckstring_matches)
            logfile.write(user, text_time, deckstring_matches)
