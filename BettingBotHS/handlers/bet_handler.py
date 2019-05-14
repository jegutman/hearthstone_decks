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
        query_res = bet_db_handler.pick(message.author, event_id, option_id, amount)
        return query_res

    def handle_show_picks(self, args, message, bet_db_handler):
        query, flags = get_args(args)
        query_res = bet_db_handler.show_picks(message.author, query)
        line_reset = 16
        
        res = []
        res.append("event_id  (p1_id) player1 @ player2 (p2_id) time\n")
        res_str = ""
        #res_str += "%5s %20s (%3s) %20s (%3s)\n" % ('id', 'option
        count = 0
        for event_id, event_name, event_time, options in query_res:
            event_name = event_name.split('_at_')[0].replace('_', ' ')
            time_str = parse_date(event_time)
            if len(options) != 2: assert False
            if len(options) == 2:
                oid1, o1 = options[0]
                oid2, o2 = options[1]
                try:
                    if event_name.index(o1) < event_name.index(o2):
                        oid1, o1, oid2, o2 = oid2, o2, oid1, o1
                except:
                    continue
                a1 = "(%(oid1)2s) %(o1)s" % locals()
                a2 = "%(o2)s (%(oid2)2s)" % locals()
                event_name = "%(a1)-16s @ %(a2)16s" % locals()
                #event_name = " @ ".join(["%(option_name)s (%(option_id)s)" % locals() for option_id, option_name in options])
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
        if count % line_reset != 0:
            res.append(res_str)
        return res
