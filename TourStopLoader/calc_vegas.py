import math

def win_odds(x):
    #series = x ** 3 + 3 * x **2 * (1-x)
    # 7-1 or better
    series = x
    top8 = series ** 12 + 12 * series ** 11 * (1-series) + 66 * series ** 10 * (1-series) ** 2 + 220 * series ** 9 * (1-series) ** 3 * 3.5/14
    series = (series - 0.5) / 2 + 0.5
    top4 = series * top8
    top2 = series * top4
    win = series * top2
    return top8, top4, top2, win

def bo5(x):
    return x**5 + 5 * x**4 * (1-x) + 10 * x**3 * (1-x) ** 2

#def win_odds(x):
#    series = x
#    # 7-1 or better
##    top8 = series ** 8 + 8 * series ** 7 * (1-series)
#    win = series ** 3 * top8
#    return win

def percent_90(x, res=0.1):
    return math.log(res) / math.log(1-win_odds(x))

for x in range(500, 925, 25):
    x = x / 1000
    pct = round(x * 100, 1)
    #tournament = round(100 * win_odds(x), 1)
    #events50 = int(round(percent_90(x, 0.5) + 0.5, 0))
    #events = int(round(percent_90(x) + 0.5, 0))
    top8, top4, top2, win = win_odds(x)
    top8, top4, top2, win = [round(100 * i, 1) for i in (top8, top4, top2, win)]
    print("%s,%s,%s,%s,%s" % (pct, top8, top4, top2, win))
