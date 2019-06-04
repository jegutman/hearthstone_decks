import requests,json
import datetime
import pytz
import sys
sys.path.append('/home/jgutman/workspace/hearthstone_decks/')
sys.path.append('/home/jgutman/workspace/hearthstone_decks/TourStopLoader')
sys.path.append('../')
from config import basedir
sys.path.append(basedir)

import MySQLdb
#import MySQLdb.constants as const
from config import *
connection = MySQLdb.connect(host='localhost', user=db_user, passwd=db_passwd, charset = 'utf8mb4')
#cursor = connection.cursor()
#cursor.execute("SET NAMES utf8")


event_ids = {}
EVENT_COUNTER = int('A000', 16)
def get_event_id(index):
    global EVENT_COUNTER, event_ids
    if index not in event_ids: 
        EVENT_COUNTER += 1
        event_ids[index] = hex(EVENT_COUNTER)[2:].upper()
    return event_ids[index]
    #return str(time) + '000' + str(region_id)

def parse_date(time):
    #return datetime.datetime.fromtimestamp(time / 1000, tz = pytz.timezone('America/Los_Angeles')).strftime("%Y-%m-%d %H:%M:%S")
    d = datetime.datetime.fromtimestamp(time / 1000, tz = pytz.timezone('America/Los_Angeles'))
    #d = d.astimezone(pytz.timezone('US/Eastern'))
    return d.strftime("%Y-%m-%d %H:%M:%S %Z")

data = json.loads(requests.get('https://playhearthstone.com/en-us/api/esports/schedule/grandmasters/?season=1&year=2019').text)

now = int(datetime.datetime.now(tz = pytz.timezone('America/Los_Angeles')).strftime('%s'))

matches = []
raw_matches = []
handles = set()
for region in [0,1,2]:
    #print("\n",region)
    for bracket in [0,1]:
        for match in sorted(data['requestedSeasonTournaments'][region]['stages'][0]['brackets'][bracket]['matches'], key=lambda x:x['startDate']):
            res = []
            res.append(match['startDate'])
            for c in match['competitors']:
                #print(c['name'], end='')
                res.append(c['name'])
            res.append(region)
            #print(parse_date(match['startDate']))
            #res.append(parse_date(match['startDate']))
            #a,b,c = res
            #print("%3s %-20s %-20s %s" % (count, a,b,c))
            #print("%3s %-20s %-20s %s" % (count, a,b,c))
            matches.append(res)
            if 'winner' in match:
                print('%-20s' % match['winner']['name'], parse_date(res[0]), res)
            else:
                print((res[0] / 1000 - now) / (24 * 3600))
            raw_matches.append(match)
            try:
                p1 = match['competitors'][0]['handle']
                p2 = match['competitors'][1]['handle']
                handles.add((p1, region))
                handles.add((p2, region))
            except:
                continue
        print("")
    print("")

event_names = []
for c,a,b, region in sorted(matches[:168]):
    event_name = "%(a)s @ %(b)s" % locals()
    if event_name in event_names: print(event_name)
    event_names.append(event_name)
print(len(event_names))
print(len(set(event_names)))

for i in handles:
    x,y = i
    print(x, y)
