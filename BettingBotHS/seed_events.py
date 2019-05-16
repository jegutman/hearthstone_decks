import sys
import datetime
from collections import defaultdict
sys.path.append('/home/jgutman/workspace/hearthstone_decks/BettingBotHS')
sys.path.append('../')
from config import basedir
sys.path.append(basedir)
import json, requests
import os
os.environ['TZ'] = 'America/Chicago'
import MySQLdb
import MySQLdb.constants as const
from config import *
connection = MySQLdb.connect(host='localhost', user=db_user, passwd=db_passwd, charset = 'utf8mb4')
#connection = MySQLdb.connect(user = 'guest', db = 'test', charset = 'utf8')
cursor = connection.cursor()
cursor.execute("SET NAMES utf8")
db = 'betting_bot'
sql = "SELECT event_id, option_id FROM %(db)s.event_options join %(db)s.events using(event_id)"
cursor.execute(sql % locals())
tid = 8
time_str = datetime.datetime.now().strftime('%s')
for i,j in cursor.fetchall():
    #print(i, j)
    tid+= 1
    bet_id = 'SEED_BET'
    from_account = 'SEED'
    to_account = 'BET-USEED-E%s-O%s' % (i, j)
    amount = 2000
    sql_txn = "INSERT INTO transactions (transaction_id, bet_id, from_account, to_account, amount, time) VALUES (%(tid)s, '%(bet_id)s', '%(from_account)s', '%(to_account)s', %(amount)s, %(time_str)s);"
    print(sql_txn % locals())
