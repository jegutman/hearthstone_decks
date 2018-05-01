import re

from sim_matchup import *
from target_utils import *

from json_win_rates import filename as wr_filename

class SimHandler():
    def __init__(self):
            pass

    def handle(self, commands, is_conquest=True):
        lineup_a, lineup_b = commands.split('" "')
        lineup_a = lineup_a.replace('"', '')
        lineup_b = lineup_b.replace('"', '')
        lineup_a = lineup_a.split(',')
        lineup_b = lineup_b.split(',')
        lineup_a = [i.strip() for i in lineup_a]
        lineup_b = [i.strip() for i in lineup_b]
        #return str(lineup_a) + str(lineup_b)
    
        if is_conquest:
            #print('`' + sim(lineup_a,lineup_b) + '`')
            return '`' + sim(lineup_a,lineup_b) + '`'
        else:
            #print('`' + sim_lhs(lineup_a,lineup_b) + '`')
            return '`' + sim_lhs(lineup_a,lineup_b) + '`'

    def handle_bans(self, commands, is_conquest=True):
        lineup_a, lineup_b = commands.split('" "')
        lineup_a = lineup_a.replace('"', '')
        lineup_b = lineup_b.replace('"', '')
        lineup_a = lineup_a.split(',')
        lineup_b = lineup_b.split(',')
        lineup_a = [i.strip() for i in lineup_a]
        lineup_b = [i.strip() for i in lineup_b]
        #return str(lineup_a) + str(lineup_b)
    
        if is_conquest:
            #print('`' + sim(lineup_a,lineup_b) + '`')
            return '`' + cq_bans(lineup_a,lineup_b) + '`'
        else:
            #print('`' + sim_lhs(lineup_a,lineup_b) + '`')
            #return '`' + sim_lhs(lineup_a,lineup_b) + '`'
            return '`LHS not supported yet`'

    #def handle_target(self, input, is_conquest=True):
    #    target_lineups = input.split('" "')
    #    target_lineups = [i.replace('"', '') for i in target_lineups]
    #    target_lineups = [i.strip() for i in target_lineups]
    #    target_lineups = [i.split(',') for i in target_lineups]
    #    for i in target_lineups:
    #        i = [j.strip() for j in i]
    #    if is_conquest:
    #        #print('`' + sim(lineup_a,lineup_b) + '`')
    #        return '`' + target(target_lineups) + '`'
    #    else:
    #        #print('`' + sim_lhs(lineup_a,lineup_b) + '`')
    #        #return '`' + sim_lhs(lineup_a,lineup_b) + '`'
    #        return

    def data_check(self):
        return '`using: %s`' % wr_filename.split('/')[-1]
