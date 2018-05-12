import json
import datetime

import re
deckstring_re = re.compile('(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{4}){12,}')

# Import the necessary methods from "twitter" library
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream

# Variables that contains the user credentials to access Twitter API 

from twitter_config import *
oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

twitter = Twitter(auth=oauth)


users_to_parse = [
    'xixohs',
    'rage_hs',
    'hsprodecks',
    'ahirun',
    'NVD_hunterace',
    'tylerootd',
    'riku97hs',
    'Furyhunterhs',
    'fireaei',
    'Gyong_hs',
    'G2Thijs',
    'liquid_hsdog',
]

for user in users_to_parse:
    for i in twitter.statuses.user_timeline(screen_name=user, count=200, tweet_mode='extended'):
        #print(i['full_text'])
        deckstring_matches = deckstring_re.findall(i['full_text'])
        if deckstring_matches:
            time = datetime.datetime.strptime(i['created_at'][:19] + i['created_at'][-5:], "%a %b %d %H:%M:%S %Y")
            text_time = time.strftime("%Y_%m_%d")
            if text_time > '2018_04_11':
                print(user, text_time, deckstring_matches)
        #print(i['full_text'])
