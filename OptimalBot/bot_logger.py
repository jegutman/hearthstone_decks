from shared_utils import *
from config import *

import logging

class BotLogger():
    def __init__(self, name='botlogger'):
        self.logger = logging.getLogger(name)
        self.handler = logging.FileHandler('OptimalBot/logs/%(name)s.log' % locals())
        self.formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        self.handler.setFormatter(formatter)
        self.logger.addHandler(hdlr) 
        self.logger.setLevel(logging.WARNING)
        
    def error_log(message):
        self.logger.error(message)
    
    def info_log(message):
        self.logger.info(message)
