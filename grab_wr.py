import requests
import pycookiecheat
from fake_useragent import UserAgent

url = 'https://hsreplay.net/analytics/query/head_to_head_archetype_matchups/?GameType=RANKED_STANDARD&RankRange=LEGEND_ONLY&Region=ALL&TimeRange=LAST_3_DAYS'
url_base = 'http://hsreplay.net'

ua = UserAgent()

#s = requests.Session()
header = {'User-Agent':str(ua.chrome)}
cookies = pycookiecheat.chrome_cookies(url_base)
htmlContent = requests.get(url, cookies = cookies, headers=header)

print(htmlContent.text)

output = open('tmp.json', 'w')
output.write(htmlContent.text)
#import requests
#
#
#print(ua.chrome)
#print(header)
#url = "https://www.hybrid-analysis.com/recent-submissions?filter=file&sort=^timestamp"
#htmlContent = requests.get(url, headers=header, cookies=cookies)
#print(htmlContent)
