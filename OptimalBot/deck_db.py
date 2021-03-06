from shared_utils import *
from config import *
from deck_manager import EasyDeck, print_side_by_side, side_by_side_diff_lines
from arg_split import get_args
import sys

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
def get_tname(tournament_number):
    if 'L' in tournament_number:
        tournament_number = tournament_number[1:]
        tournament_name = "hearthstone-masters-qualifier-las-vegas-%(tournament_number)s" % locals()
    if 'S' in tournament_number:
        tournament_number = tournament_number[1:]
        tournament_name = "hearthstone-masters-qualifier-seoul-%(tournament_number)s" % locals()
    return tournament_name

class DeckDBHandler():
    def __init__(self, logger):
        self.connection = MySQLdb.connect(host='localhost', user=db_user, passwd=db_passwd, charset = 'utf8mb4')
        self.cursor = self.connection.cursor()
        #self.cursor.execute("SET NAMES utf8")
        #self.cursor.execute("SET CHARACTER SET utf8mb4")
        #self.cursor.execute("SET character_set_connection=utf8mb4")
        self.logger = logger
        self.query_dc = "SELECT * FROM %(db)s.%(table)s WHERE deck_code = '%(deck_code)s'"
        self.query_label = "SELECT deck_code, deck_name, deck_archetype FROM %(db)s.%(table)s WHERE deck_code = '%(deck_code)s'"

    def check_cursor(self):
        try:
            cursor.execute("SELECT 1")
        except:
            self.connection = MySQLdb.connect(host='localhost', user=db_user, passwd=db_passwd, charset = 'utf8mb4')
            self.cursor = self.connection.cursor()

    def guess_archetype(self, deck):
        deck_class = deck.get_class()
        max_results = 5
        max_dist = 5
        to_compare = self.get_decks_by_class(deck_class)
        res = []
        for deck_id, deck_archetype, deck_code_tmp in to_compare:
            tmp_deck = EasyDeck(deck_code_tmp)
            distance = deck.get_distance(tmp_deck)
            res.append((distance, deck_id, deck_archetype, deck_code_tmp))
        res_final = sorted([i for i in res if i[0] <= max_dist][:max_results])
        if len(res_final) == 0:
            return None
        else:
            return res_final[0][2]
            
    def get_deck_from_id(self, deck_id):
        self.check_cursor()
        db, table = 'deckstrings,decks'.split(',')

        self.cursor.execute("SELECT deck_code, deck_name FROM %(db)s.%(table)s WHERE deck_id = %(deck_id)s" % locals())
        return self.cursor.fetchone()

    def get_name_from_code(self, deck_code):
        self.check_cursor()
        db, table = 'deckstrings,decks'.split(',')

        self.cursor.execute("SELECT deck_name FROM %(db)s.%(table)s WHERE deck_code = '%(deck_code)s'" % locals())
        res = self.cursor.fetchone()
        if not res:
            return ''
        return res[0]

    def get_decks_by_class(self, deck_class):
        self.check_cursor()
        db, table = 'deckstrings,decks'.split(',')

        self.cursor.execute("SELECT deck_id, deck_archetype, deck_code FROM %(db)s.%(table)s WHERE deck_class = '%(deck_class)s'" % locals())
        return [(i,j,k) for (i,j,k) in self.cursor.fetchall()]

    def get_record(self, player):
        self.check_cursor()
        player = player[0]
        db = 'masters_cups'
        sql = """
            SELECT player_name, count(distinct tournament_id) as cups, sum(if(result='W', 1, 0)) as wins, sum(if(result in ('W', 'L'), 1, 0)) as games
            FROM %(db)s.games join %(db)s.player_info using(tournament_id, player_id)
            WHERE player_name like '%(player)s%%'
            GROUP BY player_name
            ORDER BY cups desc, wins desc
        """
        print(sql % locals())
        self.cursor.execute(sql % locals())
        return [i for i in self.cursor.fetchall()]

    def get_cup_history(self, player):
        self.check_cursor()
        player = player[0]
        db = 'masters_cups'
        sql = """
            SELECT tournament_name, time, player_name, archetype_prim, sum(if(result='W', 1, 0)) as wins, sum(if(result in ('W', 'L'), 1, 0)) as games
            FROM %(db)s.games join %(db)s.player_info using(tournament_id, player_id) join %(db)s.tournament using(tournament_id)
            WHERE player_name like '%(player)s%%'
            GROUP BY tournament_name, time, player_name, archetype_prim
            ORDER BY time, games desc
        """
        print(sql % locals())
        self.cursor.execute(sql % locals())
        return [(i,j,k, l, m) for (i,t,j,k, l, m) in self.cursor.fetchall()]

    def get_winners(self):
        self.check_cursor()
        db = 'masters_cups'
        sql = """
            SELECT tournament_name, player_name, archetype_prim
            FROM %(db)s.winners join %(db)s.player_info using(tournament_id, player_id) join %(db)s.tournament using(tournament_id)
            ORDER BY time
        """
        print(sql % locals())
        self.cursor.execute(sql % locals())
        #print(self.cursor.fetchall())
        res = self.cursor.fetchall()
        #res = [(i.split('-')[-1], j, k) for (i,j,k) in self.cursor.fetchall()]
        res = [(str('L' if 'vegas' in i else 'S') + i.split('-')[-1], j, k) for (i,j,k) in res]
        #for i in res:
        #    print(i[1])
        return res


    def get_meta(self, tournament_numbers):
        self.check_cursor()
        db = 'masters_cups'
        tournaments = []
        if '..' in tournament_numbers[0]:
            a,b = [i for i in tournament_numbers[0].split('..')]
            start_tournament = get_tname(a)
            end_tournament = get_tname(b)
        else:
            start_tournament = tournament_numbers[0]
            end_tournament = tournament_numbers[0]
        sql = """SELECT time from %(db)s.tournament WHERE tournament_name = '%(start_tournament)s'"""
        print(sql % locals())
        self.cursor.execute(sql % locals())
        start_time = [i for (i,) in self.cursor.fetchall()][0]
        sql = """SELECT time from %(db)s.tournament WHERE tournament_name = '%(end_tournament)s'"""
        self.cursor.execute(sql % locals())
        end_time = [i for (i,) in self.cursor.fetchall()][0]
        
       #self.cursor.execute("SELECT tournament_id from tournament where tournament_name in %(tournaments)s" % locals())
        sql = """
            SELECT archetype_prim, count(*) as total
            FROM %(db)s.player_info join %(db)s.tournament using(tournament_id)
            WHERE time >= %(start_time)s and time <= %(end_time)s
            GROUP BY archetype_prim
            ORDER BY total desc
        """
        print(sql % locals())
        self.cursor.execute(sql % locals())
        return [(i,j) for (i,j) in self.cursor.fetchall()]

    def get_link(self, tournament_number):
        self.check_cursor()
        db = 'masters_cups'
        tournament_number = tournament_number[0]
       #self.cursor.execute("SELECT tournament_id from tournament where tournament_name in %(tournaments)s" % locals())
        cup_name = get_tname(tournament_number)
        sql = """
            SELECT tournament_id
            FROM %(db)s.tournament 
            WHERE tournament_name = '%(cup_name)s'
            #WHERE tournament_name = 'hearthstone-masters-qualifier-las-vegas-%(tournament_number)s'
        """
        if 'L' in tournament_number:
            link = 'https://battlefy.com/hsesports/hearthstone-masters-qualifier-las-vegas-%(tournament_number)s/%(tournament_id)s/'
        if 'S' in tournament_number:
            link = 'https://battlefy.com/hsesports/hearthstone-masters-qualifier-seoul-%(tournament_number)s/%(tournament_id)s/'
        print(sql % locals())
        self.cursor.execute(sql % locals())
        tournament_id = [i for (i,) in self.cursor.fetchall()][0]
        print(tournament_id)
        return link % locals()

    def get_cup_deck(self, args):
        self.check_cursor()
        db = 'masters_cups'
        tournament_number, player = args
        tournament_name = get_tname(tournament_number)
        sql = """
            SELECT deck1, deck2, deck3
            FROM %(db)s.player_info join %(db)s.tournament using(tournament_id)
            WHERE tournament_name = '%(tournament_name)s'
                and player_name like '%(player)s%%'
        """
        print(sql % locals())
        self.cursor.execute(sql % locals())
        res = [(i,j,k) for (i,j,k) in self.cursor.fetchall()]
        decks = [EasyDeck(i, i) for i in res[0]]
        return side_by_side_diff_lines(decks)

    def get_cup_details(self, args):
        self.check_cursor()
        db = 'masters_cups'
        tournament_number, player = args
        #tournament_name = "'hearthstone-masters-qualifier-las-vegas-%(tournament_number)s'" % locals()
        tournament_name = get_tname(tournament_number)
        bracket = 'swiss'
        sql = """
            SELECT round_number, p1.player_name, p2.player_name, score1, score2, result, p2.archetype_prim
            FROM %(db)s.games g join %(db)s.tournament t on g.tournament_id = t.tournament_id and g.bracket_id = t.%(bracket)s_bracket
                join %(db)s.player_info p1 on t.tournament_id = p1.tournament_id and g.player_id = p1.player_id
                join %(db)s.player_info p2 on t.tournament_id = p2.tournament_id and g.opponent_id = p2.player_id
            WHERE t.tournament_name = %(tournament_name)s
                and p1.player_name like '%(player)s%%'
            ORDER BY round_number
        """
        print(sql % locals())
        self.cursor.execute(sql % locals())
        res = [x for x in self.cursor.fetchall()]
        bracket = 'top8'
        print(sql % locals())
        self.cursor.execute(sql % locals())
        res += [x for x in self.cursor.fetchall()]
        #decks = [EasyDeck(i, i) for i in res[0]]
        return res

    def process_deck(self, message, deck_code, name=None, archetype=None):
        self.check_cursor()
        db, table = 'deckstrings,decks'.split(',')

        deck_code      = deck_code

        self.cursor.execute(self.query_dc % locals())
        if self.cursor.fetchone():
            self.logger.error_log('Deck Code already in DB: %s' % deck_code)
            return False
        try:
            deck = EasyDeck(deck_code)
        except:
            self.logger.error_log('Bad Deck Code: %s' % deck_code)
            return False
        time           = datetime.datetime.now().strftime('%s')
        date           = datetime.datetime.now().strftime('%Y_%m_%d')
        server         = str(message.server) + '_' + str(message.channel)
        user           = str(message.author)
        is_private     = 1 if (message.channel.name in PRIVATE_CHANNELS or message.server.name in PRIVATE_SERVERS) else 0
        
        deck_class     = deck.get_class()
        if not archetype:
            archetype = self.guess_archetype(deck)
        #deck_archetype varchar(32),
        #deck_name      varchar(32),
        return self.insert_deck(deck, time, date, server, user, is_private, deck_code, deck_class, deck_archetype=archetype, deck_name=name)

    def search_helper(self, args, flags, allow_private, query_channel, limit=0, use_playoffs=False, tags=None, min_date = '2018_10_07'):
        self.check_cursor()
        playoff_str = "playoff_region = 'None'"
        if use_playoffs:
            playoff_str = "playoff_region in ('NA', 'EU', 'APAC', 'DHATX')"
            #playoff_str = "playoff_region in ('DHATX')"
        archetype_str = 'deck_archetype like "%%%s%%"' % flags.get('archetype').replace('.*', '%') if flags.get('archetype') else ''
        class_str = "deck_class like '%%%s%%'" % flags.get('class').replace('.*', '%') if flags.get('class') else ''
        name_str = "deck_name like '%%%s%%'" % flags.get('name').replace('.*', '%') if flags.get('name') else ''
        user_str = "user like '%%%s%%'" % flags.get('user').replace('.*', '%') if flags.get('user') else ''
        date_str = "date like '%%%s%%'" % flags.get('date').replace('.*', '%') if flags.get('date') else ''
        deck_code_str = "deck_code like '%%%s%%'" % flags.get('deck_code').replace('.*', '%') if flags.get('deck_code') else ''
        private_str = "" if allow_private else " and is_private = 0"
        if allow_private:
            private_str = "and (is_private = 0 or (is_private = 1 and server like '%%%s%%'))" % query_channel
        query_str = []
        for i in [archetype_str, class_str, name_str, user_str]:
            if i: query_str.append(i)
        # make sure private str is last
        query_str = '(' + " and ".join(query_str) + ')'
        if private_str:
            query_str += private_str
        if not flags and args:
            kw = args
            #if use_playoffs:
            #    query_str = "(deck_archetype like '%%%(kw)s%%' or deck_name like '%%%(kw)s%%' or deck_class like '%%%(kw)s%%' or date like '%%%(kw)s%%' or deck_code like '%%%(kw)s%%')" % locals()
            #else:
            if tags == 'lineup':
                query_str = "(deck_archetype like \"%%%(kw)s%%\" or deck_name like \"%%%(kw)s%%\" or deck_class like \"%%%(kw)s%%\" or user like \"%%%(kw)s%%\" or date like \"%%%(kw)s%%\")" % locals()
            else:
                query_str = "(deck_archetype like \"%%%(kw)s%%\" or deck_name like \"%%%(kw)s%%\" or deck_class like \"%%%(kw)s%%\" or user like \"%%%(kw)s%%\" or date like \"%%%(kw)s%%\" or deck_code like \"%%%(kw)s%%\")" % locals()
            #if not allow_private:
            #    query_str += private_str 
            query_str += private_str 
        
        #if use_playoffs:
        #    sql_string = "SELECT deck_id, date, deck_name, deck_class, deck_code from deckstrings.playoffs where %(query_str)s"
        #else:
        #    sql_string = "SELECT deck_id, date, user, deck_name, deck_class, deck_code from deckstrings.decks where %(playoff_str)s and %(query_str)s"
        sql_string = "SELECT deck_id, date, user, deck_name, deck_class, deck_code from deckstrings.decks where %(playoff_str)s and %(query_str)s"
        sys.stdout.write(sql_string % locals())
        sys.stdout.flush()
        self.cursor.execute(sql_string % locals())
        res = []
        count = 0
        #if use_playoffs:
        #    for deck_id, date, deck_name, deck_class, deck_code in self.cursor.fetchall():
        #        count += 1
        #        res.append((deck_id, date, 'Playoffs', deck_name, deck_class, deck_code))
        #else:
        # minimum date for expansions and such
        # min_date == '2018_08_07'
        for deck_id, date, user, deck_name, deck_class, deck_code in self.cursor.fetchall():
            if date < min_date:
                continue
            count += 1
            res.append((deck_id, date, user.split('\#')[0], deck_name, deck_class, deck_code))
        if limit:
            res = res[-limit:]
        return res

    def search(self, args, flags, allow_private, query_channel, use_playoffs=False):
        res = self.search_helper(args, flags, allow_private, query_channel, use_playoffs=use_playoffs)
        #res_str = "`"
        res_str = ""
        res_str += "#%-5s %-10s %-16s %-24s %-10s \n#        %s\n" % ('id', 'date', 'user', 'deck_name', 'class', 'deck_code')
        for deck_id, date, user, deck_name, deck_class, deck_code in res[-10:]:
            user = user.split('#')[0]
            res_str += "%-6s %10s %-16s %-24s %-10s \n        %s\n" % (deck_id, date, user, deck_name, deck_class, deck_code)
        if len(res) > 10:
            res_str += '*Limited to 10 most recent results'
        #res_str += '`'
        return res_str

    def lineup(self, args, flags, allow_private, query_channel, use_playoffs=False):
        res = self.search_helper(args, flags, allow_private, query_channel, use_playoffs=use_playoffs, tags='lineup')
        all_decks = []
        res_str = []
        #for deck_id, date, user, deck_name, deck_class, deck_code in res[-10:]:
        #    res_str.append("\n".join(print_side_by_side([EasyDeck(deck_code)])))
        for deck_id, date, user, deck_name, deck_class, deck_code in sorted(res[-10:], key=lambda x:x[-2]):
            all_decks.append(EasyDeck(deck_code, deck_name))
        res_str.append("\n".join(print_side_by_side(all_decks[:int(len(all_decks)/2)])))
        res_str.append("\n".join(print_side_by_side(all_decks[int(len(all_decks)/2):])))
        #res_str = "\n".join(print_side_by_side(all_decks))
        return res_str

    def update_deck_label(self, message, deck_code, name=None, archetype=None):
        self.check_cursor()
        db, table = 'deckstrings,decks'.split(',')
        deck_name = name
        deck_archetype = archetype
        if deck_archetype: 
            deck_archetype = "'%s'" % deck_archetype
        else:
            deck_archetype = 'null'
        if deck_name: 
            deck_name = "'%s'" % deck_name
        else:
            deck_name = 'null'

        updates = []
        archetype_update = 'deck_archetype = %(deck_archetype)s' if archetype else ''
        if archetype_update:
            updates.append(archetype_update % locals())
        name_update = 'deck_name = %(deck_name)s' if name else ''
        if name_update:
            updates.append(name_update % locals())
        update_string = ", ".join(updates)
        if not update_string:
            return False

        update_query = "UPDATE %(db)s.%(table)s set %(update_string)s WHERE deck_code = '%(deck_code)s'"
        try:
            print(update_query % locals())
            self.cursor.execute(update_query % locals())
            self.connection.commit()
        except:
            self.logger.error_log('Update Failed: %(deck_code)s' % locals())
            return False
        return True
        
        
    def insert_cards(self, deck, deck_id):
        self.check_cursor()
        db = 'deckstrings'
        try:
            for card_id, quantity in deck.deck.cards:
                self.cursor.execute("INSERT INTO %(db)s.deck_to_cards (deck_id, card_id, quantity) VALUES (%(deck_id)s, %(card_id)s, %(quantity)s)" % locals())
            self.connection.commit()
        except:
            self.logger.error_log('Failed INSERT into deck_to_cards: %(deck_id)s' % locals())
            return False
        return True
    
    def insert_deck(self, deck, time, date, server, user, is_private, deck_code, deck_class, deck_archetype = None, deck_name = None):
        self.check_cursor()
        db = 'deckstrings'
        if deck_archetype: 
            deck_archetype = '"%s"' % deck_archetype
        else:
            deck_archetype = 'null'
        if deck_name: 
            deck_name = "'%s'" % deck_name
        else:
            deck_name = 'null'
        try:
            self.cursor.execute("""INSERT INTO %(db)s.decks (time, date, server, user, is_private, deck_code, deck_class, deck_archetype, deck_name)
                                   VALUES (%(time)s, '%(date)s', '%(server)s', '%(user)s', %(is_private)s, '%(deck_code)s', '%(deck_class)s', %(deck_archetype)s, %(deck_name)s)""" % locals())
            self.connection.commit()
        except:
            if not is_private:
                self.cursor.execute("""UPDATE %(db)s.decks set is_private = 0 WHERE deck_code = '%(deck_code)s'""" % locals())
            self.logger.error_log('Insert Failed: %(deck_code)s' % locals())
            return False
        try:
            self.cursor.execute("SELECT deck_id FROM %(db)s.decks WHERE deck_code = '%(deck_code)s'" % locals())
            deck_id = self.cursor.fetchone()[0]
        except:
            self.logger.error_log('Could not find code: %(deck_code)s' % locals())
            return False
        try:
            self.cursor.execute("INSERT INTO %(db)s.deck_ids (deck_id, deck_code) VALUES (%(deck_id)s, '%(deck_code)s')" % locals())
            self.connection.commit()
        except:
            self.logger.error_log('Failed Insert Into deck_ids: %(deck_id)s %(deck_code)s' % locals())
            return False
        self.insert_cards(deck, deck_id)
        return True
