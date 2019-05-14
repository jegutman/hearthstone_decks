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
            for user_id, user_name in cursor.fetchall():
                self.user_lookup[user_name] = user_id
        return self.user_lookup

    def get_transaction_id(self):
        cursor = self.cursor
        connection = self.connection
        db = 'betting_bot'
        cursor.execute("SELECT max(transaction_id) FROM %(db)s.transactions" % locals())
        max_id_tmp = [i for (i,) in cursor.fetchall()]
        if len(max_id_tmp) > 0:
            max_id = max_id_tmp[0]
        else:
            max_id = 0
        return max_id + 1
        

    def make_transfer(self, from_account, to_account, bet_id, amount):
        self.check_cursor()
        cursor = self.cursor
        connection = self.connection
        db = 'betting_bot'
        time = datetime.datetime.now().strftime('%s')
        txn_id = self.get_transaction_id()
        sql = """INSERT INTO %(db)s.transactions (transaction_id, bet_id, from_account, to_account, amount, time)
                VALUES (%(txn_id)s, '%(bet_id)s', '%(from_account)s', '%(to_account)s', %(amount)s, %(time)s)"""
        print(sql % locals())
        cursor.execute(sql % locals())
        connection.commit()
        return True
        
        

    def add_user(self, user_name):
        self.check_cursor()
        cursor = self.cursor
        db = 'betting_bot'
        users = self.get_users()
        new_uid = hex(int(max(users.values()), 16) + 1)[2:].upper()
        users[user_name] = new_uid
        print("INSERT INTO %(db)s.users (user_id, user) VALUES ('%(new_uid)s', '%(user_name)s');" % locals())
        cursor.execute("INSERT INTO %(db)s.users (user_id, user) VALUES ('%(new_uid)s', '%(user_name)s');" % locals())
        self.connection.commit()
        mt = self.make_transfer('NEW_USER', self.get_user_acct(new_uid), 'NEW', 10000)

    def get_user_acct(self, user_id):
        return 'CASH_%s' % user_id
    
    def get_bet_acct(self, user_id, event_id, option_id):
        return 'BET-U%s-E%s-O%s' % (user_id, event_id, option_id)

    def get_balances(self, user_id):
        res = defaultdict(lambda : 0)
        cursor = self.cursor
        connection = self.connection
        db = 'betting_bot'
        # check balance
        sql = """
            #SELECT sum(if(from_account = 'CASH_%(user_id)s', -amount, 0) + if(to_account = 'CASH_%(user_id)s', amount, 0)) as balance
            SELECT from_account, to_account, amount
            FROM %(db)s.transactions
            WHERE (from_account = 'CASH_%(user_id)s' or to_account = 'CASH_%(user_id)s')
            ORDER BY time
        """
        print(sql % locals())
        cursor.execute(sql % locals())
        balances = defaultdict(lambda : 0)
        for acct1, acct2, amount in cursor.fetchall():
            if user_id in acct1:
                balances[acct1] -= amount
            if user_id in acct2:
                balances[acct2] += amount
        usable_balance = balances['CASH_%(user_id)s' % locals()]
        return balances

    def available_balance(self, user_name):
        self.check_cursor()
        self.check_user(user_name)
        users = self.get_users()
        user_id = users[user_name]
        db = 'betting_bot'
        # check balance
        balances = self.get_balances(user_id)
        pending = sum([j for i,j in balances.items() if 'CASH' not in i])
        return '%s points available and %s points pending' % (balances['CASH_%(user_id)s' % locals()], pending)

    def pick(self, user_name, event_id, option_id, amount):
        try:
            amount = int(amount)
            assert amount > 0
        except:
            return "invalid amount: %s" % amount
        self.check_cursor()
        self.check_user(user_name)
        users = self.get_users()
        cursor = self.cursor
        connection = self.connection
        user_id = users[user_name]
        db = 'betting_bot'
        # check balance
        user_acct = self.get_user_acct(user_id)
        bet_acct = self.get_bet_acct(user_id, event_id, option_id)
        balances = self.get_balances(user_id)
        user_balance = balances[user_acct]
        bet_balance = balances[bet_acct]
        if amount > user_balance:
            return 'You cannot use %s, your balance is only %s' % (amount, user_balance)
        sql = """SELECT event_name, option_name FROM %(db)s.event_options join %(db)s.events using(event_id) join %(db)s.option_lookup using(option_id)
                 WHERE option_id = %(option_id)s and event_id = '%(event_id)s'"""
        try:
            print(sql % locals())
            cursor.execute(sql % locals())
            event_name, event_option = cursor.fetchall()[0]
        except:
            return 'invalid event / option combintion for event: %s option %s' % (event_id, option_id)
        mt = self.make_transfer(user_acct, bet_acct, 'BET', amount)
        balances = self.get_balances(user_id)
        new_bet_total = balances[bet_acct]
        if mt:
            return 'You have placed %s point(s) on %s in "%s"\ntotal is now %s' % (amount, event_option, event_name, new_bet_total)
        else:
            return 'something went wrong for event / option combintion for event: %s option %s' % (event_id, option_id)

    def show_picks(self, user_name, query):
        self.check_cursor()
        self.check_user(user_name)
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

    def check_user(self, user_name):
        self.check_cursor()
        cursor = self.cursor
        users = self.get_users()
        #print(user_name, users, users[user_name])
        if user_name not in users:
            self.add_user(user_name)
        return users[user_name]
