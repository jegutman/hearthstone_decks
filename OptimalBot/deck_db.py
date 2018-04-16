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
        return self.insert_deck(deck, time, date, server, user, is_private, deck_code, deck_class)
        
    def insert_cards(self, deck, deck_id):
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
        db = 'deckstrings'
        if deck_archetype: 
            deck_archetype = "'%s'" % deck_archetype
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
