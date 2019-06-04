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
EVENT_COUNTER = int('A060', 16)
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

matches = []
for region in [0,1,2]:
    #print("\n",region)
    for bracket in [0,1]:
        for match in data['requestedSeasonTournaments'][region]['stages'][0]['brackets'][bracket]['matches']:
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
count = 0
players = set()
for c,a,b, region in sorted(matches):
    count += 1
    players.add((a, region))
    players.add((b, region))
    #print("%3s %-20s %-20s %s %s" % (count, a,b,parse_date(c), region))

start_date = int(datetime.datetime.strptime('2019-06-04', '%Y-%m-%d').strftime('%s'))
end_date = int(datetime.datetime.strptime('2019-06-11', '%Y-%m-%d').strftime('%s'))
print(start_date, end_date)
#assert False

for c,a,b, region in sorted(matches)[48:]:
    sql = "INSERT INTO %(db)s.events (event_id, event_name, event_time, region_id) VALUES ('%(event_id)s', '%(event_name)s', %(event_time)s, %(region)s);"
    db = 'betting_bot'
    date_str = parse_date(c).replace(' ', '_')
    #event_name = "%(a)s_vs_%(b)s_at_%(date_str)s" % locals()
    event_name = "%(a)s @ %(b)s" % locals()
    event_id = get_event_id((c, a,b, region))
    event_time = int(c / 1000)
    if start_date <= event_time <= end_date:
        print(sql % locals())

count = 0
options = {}
for i,j in sorted(list(players), key=lambda x:(x[1], x[0].lower())):
    count += 1
    db = 'betting_bot'
    sql = "INSERT INTO %(db)s.option_lookup (option_id, option_name) VALUES (%(option_id)s, '%(option_name)s');"
    option_name = i
    option_id = count
    options[option_name] = option_id
    #print(sql % locals())
    #print(i)
#print(len(players))

for c,a,b, region in sorted(matches)[48:]:
    sql = "INSERT INTO %(db)s.events (event_id, event_name, event_time, region_id) VALUES ('%(event_id)s', '%(event_name)s', %(event_time)s, %(region)s);"
    db = 'betting_bot'
    date_str = parse_date(c).replace(' ', '_')
    #event_name = "%(a)s_vs_%(b)s_at_%(date_str)s" % locals()
    #event_id = get_event_id(c, region)
    event_id = get_event_id((c, a,b, region))
    event_time = int(c / 1000)
    #print(sql % locals())
    sql = "INSERT INTO %(db)s.event_options (event_id, option_id) VALUES ('%(event_id)s', %(option_id)s);"
    if start_date <= event_time <= end_date:
        option_id = options[a]
        print(sql % locals())
        option_id = options[b]
        print(sql % locals())
