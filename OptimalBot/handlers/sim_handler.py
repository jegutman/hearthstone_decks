import re

from sim_matchup import *
from target_utils import *
from numpy.random import choice

from json_win_rates import filenames as wr_filenames

class SimHandler():
    def __init__(self):
            pass

    def handle(self, commands, is_conquest=True):
        commands = commands.title()
        commands = commands.replace('“', '"').replace('”', '"')
        commands = commands.replace('  ', ' ')
        commands = commands.replace("echa'thun", "echathun")
        lineup_a, lineup_b = commands.split('" "')
        lineup_a = lineup_a.replace('"', '')
        lineup_b = lineup_b.replace('"', '')
        lineup_a = lineup_a.split(',')
        lineup_b = lineup_b.split(',')
        lineup_a = [i.replace("echa'Thun", "echa'thun").replace('echathun', "echa'thun").strip() for i in lineup_a]
        lineup_b = [i.replace("echa'Thun", "echa'thun").replace('echathun', "echa'thun").strip() for i in lineup_b]
        #return str(lineup_a) + str(lineup_b)
    
        if is_conquest:
            #return '`' + sim(lineup_a,lineup_b) + '`'
            return sim(lineup_a,lineup_b)
        else:
            #return '`' + sim_lhs(lineup_a,lineup_b) + '`'
            return sim_lhs(lineup_a,lineup_b)

    def handle_bans(self, commands, is_conquest=True):
        commands = commands.title()
        commands = commands.replace('“', '"').replace('”', '"')
        commands = commands.replace("echa'thun", "echathun")
        lineup_a, lineup_b = commands.split('" "')
        lineup_a = lineup_a.replace('"', '')
        lineup_b = lineup_b.replace('"', '')
        lineup_a = lineup_a.split(',')
        lineup_b = lineup_b.split(',')
        lineup_a = [i.replace('echathun', "echa'thun").strip() for i in lineup_a]
        lineup_b = [i.replace('echathun', "echa'thun").strip() for i in lineup_b]
        #return str(lineup_a) + str(lineup_b)
    
        if is_conquest:
            #return '`' + cq_bans(lineup_a,lineup_b) + '`'
            return cq_bans(lineup_a,lineup_b)
        else:
            #return '`LHS not supported yet`'
            #return 'LHS not supported yet'
            return lhs_bans(lineup_a,lineup_b)

    def handle_lead(self, commands, is_conquest=True):
        commands = commands.title()
        commands = commands.replace('“', '"').replace('”', '"')
        commands = commands.replace("echa'thun", "echathun")
        lineup_a, lineup_b = commands.split('" "')
        lineup_a = lineup_a.replace('"', '')
        lineup_b = lineup_b.replace('"', '')
        lineup_a = lineup_a.split(',')
        lineup_b = lineup_b.split(',')
        lineup_a = [i.replace('echathun', "echa'thun").strip() for i in lineup_a]
        lineup_b = [i.replace('echathun', "echa'thun").strip() for i in lineup_b]
        #return str(lineup_a) + str(lineup_b)
    
        if is_conquest:
            #return '`' + cq_bans(lineup_a,lineup_b) + '`'
            #return cq_bans(lineup_a,lineup_b)
            return 'not implemented yet'
        else:
            #return '`LHS not supported yet`'
            #return 'LHS not supported yet'
            return lhs_leads(lineup_a,lineup_b)

    def handle_nash_lead(self, commands, is_conquest=True):
        commands = commands.title()
        commands = commands.replace('“', '"').replace('”', '"')
        commands = commands.replace("echa'thun", "echathun")
        lineup_a, lineup_b = commands.split('" "')
        lineup_a = lineup_a.replace('"', '')
        lineup_b = lineup_b.replace('"', '')
        lineup_a = lineup_a.split(',')
        lineup_b = lineup_b.split(',')
        lineup_a = [i.replace('echathun', "echa'thun").strip() for i in lineup_a]
        lineup_b = [i.replace('echathun', "echa'thun").strip() for i in lineup_b]
        #return str(lineup_a) + str(lineup_b)
    
        if is_conquest:
            #return '`' + cq_bans(lineup_a,lineup_b) + '`'
            #return cq_bans(lineup_a,lineup_b)
            return 'not implemented yet'
        else:
            #return '`LHS not supported yet`'
            #return 'LHS not supported yet'
            return lhs_nash(lineup_a,lineup_b)

    def handle_nash_cq_bans(self, commands, is_conquest=True):
        commands = commands.title()
        commands = commands.replace('“', '"').replace('”', '"')
        commands = commands.replace("echa'thun", "echathun")
        lineup_a, lineup_b = commands.split('" "')
        lineup_a = lineup_a.replace('"', '')
        lineup_b = lineup_b.replace('"', '')
        lineup_a = lineup_a.split(',')
        lineup_b = lineup_b.split(',')
        lineup_a = [i.replace('echathun', "echa'thun").strip() for i in lineup_a]
        lineup_b = [i.replace('echathun', "echa'thun").strip() for i in lineup_b]
        #return str(lineup_a) + str(lineup_b)
    
        return conquest_nash_bans(lineup_a,lineup_b)

    def handle_nash_lhs_bans(self, commands, is_conquest=True):
        commands = commands.title()
        commands = commands.replace('“', '"').replace('”', '"')
        commands = commands.replace("echa'thun", "echathun")
        lineup_a, lineup_b = commands.split('" "')
        lineup_a = lineup_a.replace('"', '')
        lineup_b = lineup_b.replace('"', '')
        lineup_a = lineup_a.split(',')
        lineup_b = lineup_b.split(',')
        lineup_a = [i.replace('echathun', "echa'thun").strip() for i in lineup_a]
        lineup_b = [i.replace('echathun', "echa'thun").strip() for i in lineup_b]
        #return str(lineup_a) + str(lineup_b)
    
        if is_conquest:
            #return '`' + cq_bans(lineup_a,lineup_b) + '`'
            #return cq_bans(lineup_a,lineup_b)
            return 'not implemented yet'
        else:
            #return '`LHS not supported yet`'
            #return 'LHS not supported yet'
            return lhs_nash_bans(lineup_a,lineup_b)

    def data_check(self):
        name_info = wr_filenames[0].split('/')[-1].split('.')[0]
        name_info = name_info.replace('hsreplay', '')
        date, skill, period = name_info.split('_')
        date = date[:4] + '_' + date[4:6] + '_' + date[6:]
        if skill == 'LONLY':
            skill = 'Legend only data'
        elif skill == 'L5':
            skill = 'L-5 data'
        if len(wr_filenames) > 1:
            skill = 'blended data' 
        if period != 'EXPANSION':
            period = period[:1] + ' ' + period[1:]
            combined = "%s from %s for the previous %s" % (skill, date, period)
        else:
            combined = "%s from %s for the current expansion" % (skill, date)
        return 'using: %s' % combined
        #return 'using: %s' % wr_filename.split('/')[-1]

    def get_random(self, commands):
        commands = commands.title()
        commands = commands.replace('“', '"').replace('”', '"')
        commands = commands.split(' ')
        if len(commands) == 1:
            res = random.randint(1, int(commands[0]))
            return "%s" % res
        else:
            commands = [i + ('.0' if '.' not in i else '') for i in commands]
            print(commands)
            tmp = [float(i) for i in commands]
            normal = [i / sum(tmp) for i in tmp]
            res = "Picking from: %s" % tmp + '\n'
            #res += "%s" % normal + '\n'
            rnd = choice(range(1, len(tmp) + 1), 1, p=normal)
            res += "Choice:       %s" % [rnd[0], str(tmp[int(rnd[0])-1])]
            return res
