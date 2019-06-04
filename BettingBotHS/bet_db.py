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

def get_user_from_acct(acct):
    return acct.split('-')[1][1:]

def get_event_from_acct(acct):
    return acct.split('-')[2][1:]

def get_option_from_acct(acct):
    return acct.split('-')[3][1:]

def get_acct_details(acct):
    return (acct.split('-')[1][1:], acct.split('-')[2][1:], acct.split('-')[3][1:])

def get_player_option(acct):
    return (acct.split('-')[1][1:], acct.split('-')[3][1:])

class BettingBotDBHandler():
    def __init__(self, logger):
        self.connection = MySQLdb.connect(host='localhost', user=db_user, passwd=db_passwd, charset = 'utf8mb4')
        self.cursor = self.connection.cursor()
        self.logger = logger
        self.user_lookup = None
        self.reverse_lookup = {}

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
                self.reverse_lookup[user_id] = user_name
        return self.user_lookup

    def lookup_option(self, option_id):
        cursor = self.cursor
        db = 'betting_bot'
        print("SELECT option_name from %(db)s.option_lookup WHERE option_id = %(option_id)s" % locals())
        cursor.execute("SELECT option_name from %(db)s.option_lookup WHERE option_id = %(option_id)s" % locals())
        return [i for (i,) in cursor.fetchall()][0]

    def lookup_event(self, event_id):
        cursor = self.cursor
        db = 'betting_bot'
        print("SELECT event_name from %(db)s.events WHERE event_id = '%(event_id)s'" % locals())
        cursor.execute("SELECT event_name from %(db)s.events WHERE event_id = '%(event_id)s'" % locals())
        return [i for (i,) in cursor.fetchall()][0]

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
        self.connection.commit()
        return True

    def make_test_transfer(self, from_account, to_account, bet_id, amount):
        print('TEST TRANSFER', from_account, to_account, bet_id, amount)
        return True
        

    def add_user(self, user_name):
        self.check_cursor()
        cursor = self.cursor
        db = 'betting_bot'
        users = self.get_users()
        new_uid = hex(int(max(users.values()), 16) + 1)[2:].upper()
        users[user_name] = new_uid
        self.reverse_lookup[new_uid] = user_name
        print("INSERT INTO %(db)s.users (user_id, user) VALUES ('%(new_uid)s', '%(user_name)s');" % locals())
        cursor.execute("INSERT INTO %(db)s.users (user_id, user) VALUES ('%(new_uid)s', '%(user_name)s');" % locals())
        self.connection.commit()
        mt = self.make_transfer('NEW_USER', self.get_user_acct(new_uid), 'NEW', 10000)

    def refill(self, user_name, user_id):
        self.check_cursor()
        cursor = self.cursor
        db = 'betting_bot'
        users = self.get_users()
        balances = self.get_balances(user_id)
        user_bets = self.get_user_bets(user_id)
        pending = sum([j for i,j in user_bets.items() if 'CASH' not in i])
        #res_str =  '%s point(s) available and %s point(s) pending\n' % (balances['CASH_%(user_id)s' % locals()], pending)
        mt = self.make_transfer('REFILL', self.get_user_acct(user_id), 'REFILL', max(0, 2000 - pending - balances['CASH_%(user_id)s' % locals()]))
        return "SUCCESS"

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
        return balances

    def get_user_bets(self, user_id):
        res = defaultdict(lambda : 0)
        cursor = self.cursor
        connection = self.connection
        db = 'betting_bot'
        # check balance
        sql = """
            SELECT from_account, to_account, amount
            FROM %(db)s.transactions
            WHERE (from_account like 'BET-U%(user_id)s-%%' or to_account like 'BET-U%(user_id)s-%%')
               or (from_account like 'BET-U%(user_id)s-%%' or to_account like 'BET-U%(user_id)s-%%')
            ORDER BY time
        """
        print(sql % locals())
        cursor.execute(sql % locals())
        balances = defaultdict(lambda : 0)
        for acct1, acct2, amount in cursor.fetchall():
            if 'BET' in acct1:
                event_id1, option_id1 = acct1.split('-')[-2:]
                #if acct1.split('-')[2][1:] == event_id:
                balances[(event_id1, option_id1)] -= amount
            if 'BET' in acct2:
                event_id2, option_id2 = acct2.split('-')[-2:]
                #if acct2.split('-')[2][1:] == event_id:
                #    balances[int(acct2.split('-')[3][1:])] += amount
                balances[(event_id2, option_id2)] += amount
        print(balances)
        return balances

    def get_event_player_option_balances(self, event_id):
        res = defaultdict(lambda : 0)
        cursor = self.cursor
        connection = self.connection
        db = 'betting_bot'
        # check balance
        sql = """
            SELECT from_account, to_account, amount
            FROM %(db)s.transactions
            WHERE (from_account like 'BET%%-E%(event_id)s-%%' or to_account like 'BET%%-E%(event_id)s-%%')
            ORDER BY time
        """
        print(sql % locals())
        cursor.execute(sql % locals())
        balances = defaultdict(lambda : 0)
        for acct1, acct2, amount in cursor.fetchall():
            if 'BET' in acct1:
                if get_event_from_acct(acct1) == event_id:
                    balances[get_player_option(acct1)] -= amount
            if 'BET' in acct2:
                if get_event_from_acct(acct2) == event_id:
                    balances[get_player_option(acct2)] += amount
        print(balances)
        return balances

    def get_event_option_balances(self, event_id):
        res = defaultdict(lambda : 0)
        cursor = self.cursor
        connection = self.connection
        db = 'betting_bot'
        # check balance
        sql = """
            SELECT from_account, to_account, amount
            FROM %(db)s.transactions
            WHERE (from_account like 'BET%%-E%(event_id)s-%%' or to_account like 'BET%%-E%(event_id)s-%%')
            ORDER BY time
        """
        #print(sql % locals())
        cursor.execute(sql % locals())
        balances = defaultdict(lambda : 0)
        for acct1, acct2, amount in cursor.fetchall():
            if 'BET' in acct1:
                if acct1.split('-')[2][1:] == event_id:
                    balances[int(acct1.split('-')[3][1:])] -= amount
            if 'BET' in acct2:
                if acct2.split('-')[2][1:] == event_id:
                    balances[int(acct2.split('-')[3][1:])] += amount
        print(balances)
        return balances

    def available_balance(self, user_name):
        self.check_cursor()
        self.check_user(user_name)
        users = self.get_users()
        user_id = users[user_name]
        db = 'betting_bot'
        # check balance
        balances = self.get_balances(user_id)
        #pending = sum([j for i,j in balances.items() if 'CASH' not in i])
        res = []
        user_bets = self.get_user_bets(user_id)
        pending = sum([j for i,j in user_bets.items() if 'CASH' not in i])
        res_str =  '%s point(s) available and %s point(s) pending\n' % (balances['CASH_%(user_id)s' % locals()], pending)
        count = 0
        for i,j in user_bets.items():
            if j==0: continue
            count += 1
            res_str += '  %-28s: %-14s %6s\n' % (self.lookup_event(i[0][1:]), self.lookup_option(i[1][1:]), j)
            if count % 10 == 0:
                res.append(res_str)
                res_str = ""
        if res_str:
            res.append(res_str)
        return res

    def event_balance(self, user_name, event_id):
        self.check_cursor()
        #self.check_user(user_name)
        db = 'betting_bot'
        res = self.lookup_event(event_id) + ":\n"
        for i,j in self.get_event_option_balances(event_id).items():
            if j != 0:
                print(i,j)
                #option_id, event_id =  i.split('-')[-2:]
                #print("OID", i)
                option_id = i
                res += "%-12s : %s\n" % (self.lookup_option(option_id), j)
                #res += "%-12s : %s\n" % (self.lookup_option(option_id), j)
        return res

    def check_event(self, user_name, event_id):
        self.check_cursor()
        #self.check_user(user_name)
        users = self.get_users()
        db = 'betting_bot'
        res = self.lookup_event(event_id) + ":\n"
        for i,j in self.get_event_player_option_balances(event_id).items():
            if j != 0:
                print(i,j)
                #option_id, event_id =  i.split('-')[-2:]
                #print("OID", i)
                option_id = i[1]
                user_id = i[0]
                res += "%-20s %-12s (%s) : %s\n" % (self.reverse_lookup.get(user_id, user_id), self.lookup_option(option_id), option_id, j)
                #res += "%-12s : %s\n" % (self.lookup_option(option_id), j)
        return res

    def resolve_event(self, user_name, event_id, winner_id):
        self.check_cursor()
        #self.check_user(user_name)
        users = self.get_users()
        db = 'betting_bot'
        # STEPS:
        # reason-type resolve
        # 0) Check existing winner?
        # 1) Calculate total pool
        # 2) Calculate pool of non-seed players
        # 3) Calculate transfers and make for players
        # 4) Transfer out SEED as well
        # 5) Record winner
        #res = self.lookup_event(event_id) + ":\n"
        print("SELECT event_id, option_id from %(db)s.event_winner WHERE event_id = '%(event_id)s'" % locals())
        self.cursor.execute("SELECT event_id, option_id from %(db)s.event_winner WHERE event_id = '%(event_id)s'" % locals())
        check_winner = [i for (i,) in self.cursor.fetchall()]
        if len(check_winner) > 0:
            return "Already resolved"
        self.cursor.execute("SELECT option_id FROM %(db)s.event_options WHERE event_id = '%(event_id)s'" % locals())
        options = [int(i) for (i,) in self.cursor.fetchall()]
        if int(winner_id) not in options:
            return "Invalid resolve option: %s %s" % (winner_id, options)
        total = 0
        total_non_seed = 0
        total_winners = 0
        winning_players = {}
        losing_players = {}
        seed_totals = {}
        for i,j in self.get_event_player_option_balances(event_id).items():
            if j != 0:
                print(i,j)
                #print("OID", i)
                oid = i[1]
                user_id = i[0]
                total += j
                if oid == winner_id and user_id != 'SEED':
                    total_winners += j
                    winning_players[user_id] = j
                elif oid != winner_id and user_id != 'SEED':
                    losing_players[(user_id, oid)] = j
                else:
                    seed_totals[(user_id, oid)] = j
        print('PROPOSED', total, total_winners)
        total_paid = 0
        for i,j in winning_players.items():
            to_pay = int(round(j * float(total) / total_winners, 0))
            initial_bet = j
            total_paid += to_pay
            print(self.reverse_lookup[i], j, int(round(j * float(total) / total_winners, 0)))
            user_acct = self.get_user_acct(i)
            bet_acct = self.get_bet_acct(i, event_id, winner_id)
            #mt = self.make_test_transfer(bet_acct, user_acct, 'RESOLVE-' + event_id, initial_bet)
            #mt = self.make_test_transfer('POOL-' + event_id, user_acct, 'RESOLVE-' + event_id, to_pay - initial_bet)
            mt = self.make_transfer(bet_acct, user_acct, 'RESOLVE-' + event_id, initial_bet)
            mt = self.make_transfer('POOL-' + event_id, user_acct, 'RESOLVE-' + event_id, to_pay - initial_bet)
        for i,j in losing_players.items():
            initial_bet = j
            oid = i[1]
            uid = i[0]
            bet_acct = self.get_bet_acct(uid, event_id, oid)
            #mt = self.make_test_transfer(bet_acct, 'POOL-' + event_id, 'RESOLVE-' + event_id, initial_bet)
            mt = self.make_transfer(bet_acct, 'POOL-' + event_id, 'RESOLVE-' + event_id, initial_bet)
        for i,j in seed_totals.items():
            initial_bet = j
            oid = i[1]
            uid = i[0]
            bet_acct = self.get_bet_acct(uid, event_id, oid)
            #mt = self.make_test_transfer(bet_acct, 'POOL-' + event_id, 'RESOLVE-' + event_id, initial_bet)
            mt = self.make_transfer(bet_acct, 'POOL-' + event_id, 'RESOLVE-' + event_id, initial_bet)
        print("TOTAL PAID:", total_paid)
        self.cursor.execute("INSERT INTO %(db)s.event_winner (event_id, option_id) VALUES ('%(event_id)s', %(winner_id)s)" % locals())
        self.connection.commit()
        return "default"

    def get_user(self, user_id):
        self.check_cursor()
        users = self.get_users()

    def pick(self, user_name, event_id, option_id, amount):
        event_id = event_id.upper()
        #try:
        #    amount = int(amount)
        #    assert amount > 0
        #except:
        #    return "invalid amount: %s" % amount
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
        try:
            amount = int(amount)
            assert amount >= -bet_balance
            assert not (amount == 0 and bet_balance == 0)
        except:
            return "invalid amount: %s bet_balance: %s" % (amount, bet_balance)
        if amount > user_balance:
            return 'You cannot use %s, your balance is only %s' % (amount, user_balance)
        sql = """SELECT event_name, option_name, event_time FROM %(db)s.event_options join %(db)s.events using(event_id) join %(db)s.option_lookup using(option_id)
                 WHERE option_id = %(option_id)s and event_id = '%(event_id)s'"""
        try:
            print(sql % locals())
            cursor.execute(sql % locals())
            event_name, event_option, time = cursor.fetchall()[0]
            now = int(datetime.datetime.now().strftime('%s'))
            print("TIME_DIFF", time - now)
            if time - now < 900:
                return "Sorry you cannot place points on a match that is scheduled less than 15 minutes away"
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
        print(sql % locals())
        cursor.execute(sql % locals())
        res = []
        sql = """
            SELECT option_id, option_name
            FROM %(db)s.event_options join %(db)s.option_lookup using(option_id)
            WHERE event_id = '%(event_id)s'
        """
        count = 0
        for event_id, event_name, event_time, region_name in cursor.fetchall():
            count += 1
            print(count, 'EVENT_ID', event_id)
            balances = self.get_event_option_balances(event_id)
            cursor.execute(sql % locals())
            options = [(a,b) for (a,b) in cursor.fetchall()]
            res.append((event_id, event_name, event_time, options, balances))
        return res

    def leader(self, user_name):
        self.check_cursor()
        self.check_user(user_name)
        users = self.get_users()
        db = 'betting_bot'
        user_totals = defaultdict(lambda : 0)
        sql = """
            SELECT from_account, to_account, amount
            FROM %(db)s.transactions
            ORDER BY time
        """
        #print(sql % locals())
        self.cursor.execute(sql % locals())
        count = 0
        for from_acct, to_acct, amount in self.cursor.fetchall():
            count += 1
            for user_id in users.values():
                if user_id == 'A00001': continue
                if user_id in from_acct:
                    user_totals[user_id] -= amount
                    print('fr', count, user_id)
                if user_id in to_acct:
                    user_totals[user_id] += amount
                    print('to', count, user_id)
        res_str = ""
        for i,j in sorted(user_totals.items(), key=lambda x:x[1], reverse=True)[:10]:
            res_str += "%-20s %6s\n" % (self.reverse_lookup[i], j)
        for i,j in sorted(user_totals.items(), key=lambda x:x[1], reverse=True):
            print(i, "%-20s %6s\n" % (self.reverse_lookup[i], j))
        return res_str

    def check_user(self, user_name):
        self.check_cursor()
        cursor = self.cursor
        users = self.get_users()
        #print(user_name, users, users[user_name])
        if user_name not in users:
            self.add_user(user_name)
        return users[user_name]
