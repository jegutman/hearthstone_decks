import re

from sim_matchup import *
from target_utils import *

from json_win_rates import filename as wr_filename

class SimHandler():
    def __init__(self):
            pass

    def handle(self, commands, is_conquest=True):
        commands = commands.replace('“', '"').replace('”', '"')
        lineup_a, lineup_b = commands.split('" "')
        lineup_a = lineup_a.replace('"', '')
        lineup_b = lineup_b.replace('"', '')
        lineup_a = lineup_a.split(',')
        lineup_b = lineup_b.split(',')
        lineup_a = [i.strip() for i in lineup_a]
        lineup_b = [i.strip() for i in lineup_b]
        #return str(lineup_a) + str(lineup_b)
    
        if is_conquest:
            #return '`' + sim(lineup_a,lineup_b) + '`'
            return sim(lineup_a,lineup_b)
        else:
            #return '`' + sim_lhs(lineup_a,lineup_b) + '`'
            return sim_lhs(lineup_a,lineup_b)

    def handle_bans(self, commands, is_conquest=True):
        commands = commands.replace('“', '"').replace('”', '"')
        lineup_a, lineup_b = commands.split('" "')
        lineup_a = lineup_a.replace('"', '')
        lineup_b = lineup_b.replace('"', '')
        lineup_a = lineup_a.split(',')
        lineup_b = lineup_b.split(',')
        lineup_a = [i.strip() for i in lineup_a]
        lineup_b = [i.strip() for i in lineup_b]
        #return str(lineup_a) + str(lineup_b)
    
        if is_conquest:
            #return '`' + cq_bans(lineup_a,lineup_b) + '`'
            return cq_bans(lineup_a,lineup_b)
        else:
            #return '`LHS not supported yet`'
            #return 'LHS not supported yet'
            return lhs_bans(lineup_a,lineup_b)

    def handle_lead(self, commands, is_conquest=True):
        commands = commands.replace('“', '"').replace('”', '"')
        lineup_a, lineup_b = commands.split('" "')
        lineup_a = lineup_a.replace('"', '')
        lineup_b = lineup_b.replace('"', '')
        lineup_a = lineup_a.split(',')
        lineup_b = lineup_b.split(',')
        lineup_a = [i.strip() for i in lineup_a]
        lineup_b = [i.strip() for i in lineup_b]
        #return str(lineup_a) + str(lineup_b)
    
        if is_conquest:
            #return '`' + cq_bans(lineup_a,lineup_b) + '`'
            #return cq_bans(lineup_a,lineup_b)
            return 'not implemented yet'
        else:
            #return '`LHS not supported yet`'
            #return 'LHS not supported yet'
            return lhs_leads(lineup_a,lineup_b)

    def data_check(self):
        #return '`using: %s`' % wr_filename.split('/')[-1]
        name_info = wr_filename.split('/')[-1].split('.')[0]
        name_info = name_info.replace('hsreplay', '')
        date, skill, period = name_info.split('_')
        date = date[:4] + '_' + date[4:6] + '_' + date[6:]
        if skill == 'LONLY':
            skill = 'L Only'
        elif skill == 'L5':
            skill = 'L-5'
        period = period[:1] + ' ' + period[1:]
        combined = "%s from %s for %s" % (skill, date, period)
        return 'using: %s' % combined
        #return 'using: %s' % wr_filename.split('/')[-1]
