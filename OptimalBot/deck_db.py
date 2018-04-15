from shared_utils import *
from config import *
from deck_manager import EasyDeck
import sys

import MySQLdb
import datetime
#MySQLdb.connect(host='localhost', user='loader', passwd='bhtrader')

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

class DeckDBHandler():
    def __init__(self, logger):
        self.connection = MySQLdb.connect(host='localhost', user='loader', passwd='bhtrader')
        self.cursor = self.connection.cursor()
        self.logger = logger
        self.query_dc = "SELECT * FROM %(db)s.%(table)s WHERE deck_code = '%(deck_code)s'"
        
    def process_deck(self, message, deck_code, name=None):
        # TODO: Check the deck not already in database
        db, table = 'deckstrings,decks'.split(',')
        self.cursor.execute(self.query_dc % locals())
        if self.cursor.fetchone():
            self.logger.error_log('Deck Code already in DB: %s' % deck_code)
            return False
        deck_code      = deck_code
        try:
            deck = EasyDeck(deck_code)
        except:
            self.logger.error_log('Bad Deck Code: %s' % deck_code)
            return False
        time           = datetime.datetime.now().strftime('%s')
        date           = datetime.datetime.now().strftime('%Y_%m_%d')
        server         = str(message.server) + '_' + str(message.channel)
        user           = str(message.author)
        is_private     = 1 if (message.channel.name in ['spooky'] or message.server.name == 'R N G') else 0
        
        deck_class     = deck.get_class()
        #deck_archetype varchar(32),
        #deck_name      varchar(32),
        return self.insert_deck(time, date, server, user, is_private, deck_code, deck_class)
        
    
    def insert_deck(self, time, date, server, user, is_private, deck_code, deck_class, deck_archetype = None, deck_name = None):
        db, table = 'deckstrings,decks'.split(',')
        if deck_archetype: 
            deck_archetype = "'%s'" % deck_archetype
        else:
            deck_archetype = 'null'
        if deck_name: 
            deck_name = "'%s'" % deck_name
        else:
            deck_name = 'null'
        #sys.stdout.write("""INSERT INTO %(db)s.%(table)s       (time, date, server, user, is_private, deck_code, deck_class, deck_archetype, deck_name)
        #               VALUES (%(time)s, '%(date)s', '%(server)s', '%(user)s', %(is_private)s, '%(deck_code)s', '%(deck_class)s', %(deck_archetype)s, %(deck_name)s)""" % locals())
        self.cursor.execute("""INSERT INTO %(db)s.%(table)s      (time, date, server, user, is_private, deck_code, deck_class, deck_archetype, deck_name)
                               VALUES (%(time)s, '%(date)s', '%(server)s', '%(user)s', %(is_private)s, '%(deck_code)s', '%(deck_class)s', %(deck_archetype)s, %(deck_name)s)""" % locals())
        self.connection.commit()
        return True
