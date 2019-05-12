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

    def handle_show_picks(self, args, message, bet_db_handler):
        query, flags = get_args(args)
        query_res = bet_db_handler.show_picks(message.author, query)
        line_reset = 16
        
        res = []
        res_str = ""
        #res_str += "%5s %20s (%3s) %20s (%3s)\n" % ('id', 'option
        count = 0
        for event_id, event_name, event_time, options in query_res:
            event_name = event_name.split('_at_')[0].replace('_', ' ')
            time_str = parse_date(event_time)
            res_str += "%(event_id)6s %(event_name)-24s %(time_str)s\n" % locals()
            res_str += "    "
            for option_id, option_name in options:
                res_str += "%(option_id)3s %(option_name)-12s" % locals()
            res_str += '\n'
            count += 1
            if count % line_reset == 0:
                res.append(res_str)
                res_str = ""
        if count % line_reset != 0:
            res.append(res_str)
        return res
