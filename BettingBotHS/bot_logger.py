from shared_utils import *
from config import *

import logging

class BotLogger():
    def __init__(self, name='bb_logger'):
        self.logger = logging.getLogger(name)
        self.handler = logging.FileHandler(basedir + '/BettingBotHS/logs/%(name)s.log' % locals())
        self.formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler) 
        self.logger.setLevel(logging.INFO)
        
    def error_log(self, message):
        self.logger.error(message)
    
    def info_log(self, message):
        self.logger.info(message)
