import requests
import pycookiecheat
from fake_useragent import UserAgent
import datetime
import sys
sys.path.append('../')
from config import basedir


LEVELS = ['LEGEND_ONLY', 'LEGEND_THROUGH_FIVE']
RANGE = ['LAST_1_DAY', 'LAST_3_DAYS', 'LAST_7_DAYS']

downloads = [
    ('LEGEND_ONLY', 'LAST_1_DAY'),
    ('LEGEND_ONLY', 'LAST_3_DAYS'),
    ('LEGEND_ONLY', 'LAST_7_DAYS'),
    ('LEGEND_THROUGH_FIVE', 'LAST_1_DAY'),
    ('LEGEND_THROUGH_FIVE', 'LAST_3_DAYS'),
    ('LEGEND_THROUGH_FIVE', 'LAST_7_DAYS'),
]

name_map = {
    'LEGEND_ONLY'         : 'LONLY',
    'LEGEND_THROUGH_FIVE' : 'L5',
    'LAST_7_DAYS'         : '7DAYS',
    'LAST_3_DAYS'         : '3DAYS',
    'LAST_1_DAY'          : '1DAY',
}
    

def get_filename(ranks, time):
    ranks, time = name_map[ranks], name_map[time]
    datestr = datetime.datetime.now().strftime("%Y%m%d")
    return basedir + '/lineupSolver/win_rates/hsreplay%(datestr)s_%(ranks)s_%(time)s.json' % vars()

def get_all_filename(ranks, time):
    ranks, time = name_map[ranks], name_map[time]
    datestr = datetime.datetime.now().strftime("%Y%m%d")
    hourstr = datetime.datetime.now().strftime("%H%M%S")
    return basedir + '/lineupSolver/all_wrs/hsreplay%(datestr)s_%(ranks)s_%(time)s_%(hourstr)s.json' % vars()
    


url = 'https://hsreplay.net/analytics/query/head_to_head_archetype_matchups/?GameType=RANKED_STANDARD&RankRange=%(ranks)s&Region=ALL&TimeRange=%(time_range)s'
url_base = 'http://hsreplay.net'

ua = UserAgent()

#s = requests.Session()
header = {'User-Agent':str(ua.chrome)}
cookies = pycookiecheat.chrome_cookies(url_base)
for ranks, time_range in downloads:
    htmlContent = requests.get(url % locals(), cookies = cookies, headers=header)
    filename = get_filename(ranks, time_range)
    output = open(filename, 'w')
    output.write(htmlContent.text)
    print("writing %(filename)s" % locals())
    output.close()
    output = open(get_all_filename(ranks, time_range), 'w')
    output.write(htmlContent.text)
    output.close()
