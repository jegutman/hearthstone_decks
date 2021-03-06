from config import *
import re
import sys
from arg_split import get_args
import datetime
import pytz

def parse_date(time):
    d = datetime.datetime.fromtimestamp(time, tz = pytz.timezone('America/Los_Angeles'))
    #return d.strftime("%Y-%m-%d %H:%M:%S %Z")
    return d.strftime("%m-%d %H:%M %Z")

class BetHandler():
    def __init__(self):
        pass

    def handle_pick(self, args, message, bet_db_handler):
        pick_info, flags = get_args(args)
        if len(pick_info) != 3:
            return "Format: !pick <event_id> <option_id> <amount>"
        event_id, option_id, amount = pick_info[0], pick_info[1], pick_info[2]
        #try:
        #    event_id, option_id, amount = pick_info[0], pick_info[1], pick_info[2]
        #except:
        #    print("invalid format:", message.author, pick_info)
        #    return "Format: !pick <event_id> <option_id> <amount>"
        user_name = str(message.author)
        query_res = bet_db_handler.pick(user_name, event_id, option_id, amount)
        return query_res

    def handle_balance(self, args, message, bet_db_handler):
        query, flags = get_args(args)
        user_name = str(message.author)
        return bet_db_handler.available_balance(user_name)

    def handle_leader(self, args, message, bet_db_handler):
        query, flags = get_args(args)
        user_name = str(message.author)
        return bet_db_handler.leader(user_name)

    def handle_event_balance(self, args, message, bet_db_handler):
        query, flags = get_args(args)
        user_name = str(message.author)
        return bet_db_handler.event_balance(user_name, query[0])

    def handle_check_event(self, args, message, bet_db_handler):
        query, flags = get_args(args)
        user_name = str(message.author)
        return bet_db_handler.check_event(user_name, query[0])

    def handle_resolve_event(self, args, message, bet_db_handler):
        query, flags = get_args(args)
        user_name = str(message.author)
        if 'MegaManMusic#2753' != user_name:
            return "invalid user: %s" % user_name
        return bet_db_handler.resolve_event(user_name, query[0], query[1])

    def handle_refill(self, args, message, bet_db_handler):
        query, flags = get_args(args)
        user_name = str(message.author)
        if 'MegaManMusic#2753' != user_name:
            return "invalid user: %s" % user_name
        return bet_db_handler.refill(user_name, query[0])

    def handle_show_picks(self, args, message, bet_db_handler):
        query, flags = get_args(args)
        user_name = str(message.author)
        query_res = bet_db_handler.show_picks(user_name, query)
        line_reset = 16
        
        res = []
        res.append("event_id  (p1_id) player1 <current_points> @ <current_points> player2 (p2_id) time\n")
        res_str = ""
        #res_str += "%5s %20s (%3s) %20s (%3s)\n" % ('id', 'option
        count = 0
        print("RES2", len(query_res))
        for event_id, event_name, event_time, options, balances in query_res:
            event_name = event_name.split('_at_')[0].replace('_', ' ')
            time_str = parse_date(event_time)
            #if len(options) != 2: assert False
            if len(options) == 2:
                oid1, o1 = options[0]
                oid2, o2 = options[1]
                print(event_id, event_name, event_time, len(options), o1, o2)
                if event_name.lower().index(o1.lower()) < event_name.lower().index(o2.lower()):
                    oid1, o1, oid2, o2 = oid2, o2, oid1, o1
                #try:
                #    if event_name.index(o1) < event_name.index(o2):
                #        oid1, o1, oid2, o2 = oid2, o2, oid1, o1
                #except:
                #    continue
                a1 = "(%(oid1)2s) %(o1)s" % locals()
                a2 = "%(o2)s (%(oid2)2s)" % locals()
                #print(balances)
                b1 = "%6s" % balances[oid1]
                b2 = "%6s" % balances[oid2]
                event_name = "%(a1)-16s %(b1)s @ %(b2)s %(a2)16s" % locals()
                #event_name = " @ ".join(["%(option_name)s (%(option_id)s)" % locals() for option_id, option_name in options])
            else:
                return "Failed"
            #event_name = " @ ".join(["%(option_name)s (%(option_id)s)" % locals() for option_id, option_name in options])
            #res_str += "%(event_id)4s   %(event_name)-24s %(time_str)s\n" % locals()
            res_str += "%(event_id)4s  %(event_name)-34s  %(time_str)s\n" % locals()
            #res_str += "    "
            #for option_id, option_name in options:
            #    res_str += "%(option_id)3s %(option_name)-12s" % locals()
            #res_str += '\n'
            count += 1
            if count % line_reset == 0:
                res.append(res_str)
                res_str = ""
        if res_str:
        #if count % line_reset != 0:
            res.append(res_str)
        return res
