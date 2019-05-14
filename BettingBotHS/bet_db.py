from shared_utils import *
from config import *
from deck_manager import EasyDeck, print_side_by_side, side_by_side_diff_lines
from arg_split import get_args
import sys
from collections import defaultdict

import MySQLdb
import datetime

#CREATE TABLE decks
#(
#    deck_id        int(11) NOT NULL auto_increment,
#    time           int(32) NOT NULL,
#    date           varchar(10) NOT NULL,
#    server         varchar(32) NOT NULL,
#    user           varchar(32) NOT NULL,
#    deck_name      varchar(32),
#    deck_archetype varchar(32),
#    deck_class     varchar(8) NOT NULL,
#    deck_code      varchar(128) NOT NULL,
#    PRIMARY KEY(deck_id)
#)

class BettingBotDBHandler():
    def __init__(self, logger):
        self.connection = MySQLdb.connect(host='localhost', user=db_user, passwd=db_passwd, charset = 'utf8mb4')
        self.cursor = self.connection.cursor()
        self.logger = logger
        self.user_lookup = None

    def check_cursor(self):
        try:
            self.cursor.execute("SELECT 1")
        except:
            self.connection = MySQLdb.connect(host='localhost', user=db_user, passwd=db_passwd, charset = 'utf8mb4')
            self.cursor = self.connection.cursor()

    def get_users(self):
        #self.check_cursor()
        cursor = self.cursor
        db = 'betting_bot'
        if self.user_lookup is None:
            self.user_lookup = {}
            cursor.execute("SELECT user_id, user FROM %(db)s.users" % locals())
            for user_id, user in cursor.fetchall():
                self.user_lookup[user] = user_id
        return self.user_lookup

    def add_user(self, user):
        self.check_cursor()
        cursor = self.cursor
        db = 'betting_bot'
        users = self.get_users()
        new_uid = hex(int(max(users.values()), 16) + 1)[2:].upper()
        users[user] = new_uid
        print("INSERT INTO %(db)s.users (user_id, user) VALUES ('%(new_uid)s', '%(user)s');" % locals())
        cursor.execute("INSERT INTO %(db)s.users (user_id, user) VALUES ('%(new_uid)s', '%(user)s');" % locals())
        self.connection.commit()

    def get_user_acct(self, user_id):
        return 'CASH_%s' % user_id
    
    def get_bet_acct(self, user_id, event_id, option_id):
        return 'BET-U%s-E%s-O%s' % (user_id, event_id, option_id)

    def pick(self, user, event_id, option_id, amount):
        try:
            amount = int(amount)
            assert amount > 0
        except:
            return "invalid amount: %s" % amount
        self.check_cursor()
        self.check_user(user)
        users = self.get_users()
        cursor = self.cursor
        connection = self.connection
        user_id = users[user]
        db = 'betting_bot'
        # check balance
        sql = """
            #SELECT sum(if(from_account = 'user_%(user_id)s', -amount, 0) + if(to_account = 'user_%(user_id)s', amount, 0)) as balance
            SELECT from_account, to_account, amount
            FROM %(db)s.transactions
            WHERE (from_account = 'user_%(user_id)s' or to_account = 'user_(user_id)s')
            ORDER BY time
        """
        cursor.execute(sql % locals())
        balances = defaultdict(lambda : 0)
        for acct1, acct2, amount in cursor.fetchall():
            if user_id in acct1:
                balances[acct1] -= amount
            if user_id in acct2:
                balances[acct2] += amount
        usable_balance = balances['user_%(user_id)s' % locals()]
        bet_balance = balances[self.get_bet_acct(user_id, event_id, option_id)]
        return 'test'

            
            

    def show_picks(self, user, query):
        self.check_cursor()
        self.check_user(user)
        cursor = self.cursor
        #if not query[0]: query = '%'
        if not query: query = '%'
        else: query = query[0]
        db = 'betting_bot'

        sql = """
            SELECT event_id, event_name, event_time, region_name
            FROM %(db)s.events join %(db)s.regions using(region_id)
            WHERE event_id not in (SELECT event_id FROM %(db)s.event_winner)
                and region_name like '%(query)s'
            ORDER BY region_id, event_time
        """
        cursor.execute(sql % locals())
        res = []
        sql = """
            SELECT option_id, option_name
            FROM %(db)s.event_options join %(db)s.option_lookup using(option_id)
            WHERE event_id = '%(event_id)s'
        """
        for event_id, event_name, event_time, region_name in cursor.fetchall():
            cursor.execute(sql % locals())
            options = [(a,b) for (a,b) in cursor.fetchall()]
            res.append((event_id, event_name, event_time, options))
        return res

    def check_user(self, user):
        self.check_cursor()
        cursor = self.cursor
        users = self.get_users()
        if user not in users:
            self.add_user(user)
        return users[user]
