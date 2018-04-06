from json_win_rates import * 
from conquest_utils import win_rates_lines as cq_win_rates_lines
from conquest_utils import post_ban as cq_post_ban
from conquest_utils import win_rate as cq_win_rate
from conquest_utils import pre_ban as cq_pre_ban
from conquest_utils import pre_ban_old as cq_pre_ban_old
from lhs_utils import win_rates_lines as lhs_win_rates_lines
from lhs_utils import win_rate as lhs_win_rate
from lhs_utils import pre_ban as lhs_pre_ban
from shared_utils import *

win_pcts, num_games, game_count, archetypes, overall_wr = get_win_pcts(min_game_threshold=0, min_game_count=0)

def sim(my_lineup, opp_lineup):
    res = ""
    #assert all([d in archetypes for d in my_lineup]), ([d in archetypes for d in my_lineup], my_lineup)
    for d in my_lineup:
        if d not in archetypes:
            return 'Could not recognize archetype: "%s"' % d
    for d in opp_lineup:
        if d not in archetypes:
            return 'Could not recognize archetype: "%s"' % d
    #assert all([d in archetypes for d in opp_lineup]), ([d in archetypes for d in opp_lineup], opp_lineup)

    res += str(my_lineup) +  " vs " + str(opp_lineup) + '\n'
    res += cq_win_rates_lines(my_lineup, opp_lineup, win_pcts,num_games) + '\n'
    res += str(cq_win_rate(my_lineup, opp_lineup, win_pcts)) + '\n'
    res += str(cq_pre_ban(my_lineup, opp_lineup, win_pcts)) + '\n'

    #res_ban = cq_pre_ban_old(my_lineup,
    #                         opp_lineup,
    #                         win_pcts)
    return res

def sim_lhs(my_lineup, opp_lineup):
    res = ""
    assert all([d in archetypes for d in my_lineup]), ([d in archetypes for d in my_lineup], my_lineup)
    assert all([d in archetypes for d in opp_lineup]), ([d in archetypes for d in opp_lineup], opp_lineup)

    res +=  str(my_lineup) +  " vs " + str(opp_lineup) + '\n'
    res += lhs_win_rates_lines(my_lineup, opp_lineup, win_pcts,num_games) + '\n'
    res += str(lhs_win_rate(my_lineup, opp_lineup, win_pcts)) + '\n'
    res += str(lhs_pre_ban(my_lineup, opp_lineup, win_pcts)) + '\n'

    #res_ban = lhs_pre_ban_old(my_lineup,
    #                          opp_lineup,
    #                          win_pcts)
    return res
