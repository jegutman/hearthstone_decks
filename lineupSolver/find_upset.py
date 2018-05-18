import sys
sys.path.append('../')
from config import basedir
sys.path.append(basedir)
sys.path.append(basedir + '/lineupSolver')


from shared_utils import *
from json_win_rates import * 
from conquest_utils import * 

from random import shuffle

#from hct_europe_pairings import *
from hct_americas_pairings import *

eu_decks = {
    'AA_TEST'            : ['Spiteful Druid', 'Even Paladin', 'Quest Rogue', 'Cube Warlock'],
    'AA_TEST2'           : ['Spiteful Druid','Murloc Paladin','Quest Rogue','Cube Warlock'],
    'AA_TEST3'           : ['Spiteful Druid','Murloc Paladin','Tempo Mage','Cube Warlock'],
    'AA_TEST4'           : ['Spiteful Druid','Tempo Mage','Even Paladin','Cube Warlock'],
    'A83650#2106'        : ['Spiteful Druid', 'Murloc Paladin', 'Control Priest', 'Control Warlock'],
    'Babon#21904'        : ['Spiteful Druid', 'Control Priest', 'Cube Warlock', 'Odd Quest Warrior'],
    'BoarControl#2986'   : ['Spiteful Druid', 'Tempo Mage', 'Even Paladin', 'Cube Warlock'],
    'Bozzzton#2511'      : ['Tempo Mage', 'Murloc Paladin', 'Odd Rogue', 'Cube Warlock'],
    'Bunnyhoppor#2897'   : ['Spiteful Druid', 'Tempo Mage', 'Even Paladin', 'Cube Warlock'],
    'Casie#2884'         : ['Taunt Druid', 'Control Priest', 'Miracle Rogue', 'Cube Warlock'],
    'Crane333#2314'      : ['Big Spell Mage', 'Even Paladin', 'Cube Warlock', 'Odd Warrior'],
    'Duarte#21328'       : ['Token Druid', 'Spell Hunter', 'Odd Paladin', 'Odd Warrior'],
    'ElMachico#2287'     : ['Tempo Mage', 'Even Paladin', 'Odd Rogue', 'Cube Warlock'],
    'Faeli#2572'         : ['Taunt Druid', 'Even Paladin', 'Control Priest', 'Control Warlock'],
    'Findan#2596'        : ['Spiteful Druid', 'Control Priest', 'Quest Rogue', 'Control Warlock'],
    'Fox#29320'          : ['Big Spell Mage', 'Control Priest', 'Control Warlock', 'Odd Quest Warrior'],
    'Glaser#2196'        : ['Spiteful Druid', 'Even Paladin', 'Control Priest', 'Control Warlock'],
    'Hypno#22145'        : ['Spiteful Druid', 'Tempo Mage', 'Quest Rogue', 'Cube Warlock'],
    'Jarla#21553'        : ['Taunt Druid', 'Even Paladin', 'Control Priest', 'Control Warlock'],
    'Juristis#2130'      : ['Odd Hunter', 'Tempo Mage', 'Murloc Paladin', 'Odd Rogue'],
    'Kalas#2638'         : ['Even Paladin', 'Control Priest', 'Control Warlock', 'Odd Warrior'],
    'Kalaxz#2721'        : ['Taunt Druid', 'Combo Priest', 'Quest Rogue', 'Control Warlock'],
    'Kolento#2266'       : ['Taunt Druid', 'Even Paladin', 'Control Warlock', 'Odd Warrior'],
    'Leta#21458'         : ['Spiteful Druid', 'Tempo Mage', 'Quest Rogue', 'Cube Warlock'],
    'MM78#2809'          : ['Taunt Druid', 'Control Priest', 'Control Warlock', 'Odd Warrior'],
    'Maur1#2225'         : ['Control Priest', 'Miracle Rogue', 'Cube Warlock', 'Odd Quest Warrior'],
    'Maverick#2233'      : ['Taunt Druid', 'Control Priest', 'Control Warlock', 'Odd Warrior'],
    'Meati#2841'         : ['Spiteful Druid', 'Tempo Mage', 'Even Paladin', 'Quest Rogue'],
    'Mryagut#2306'       : ['Taunt Druid', 'Control Priest', 'Quest Rogue', 'Cube Warlock'],
    'Nicslay#2567'       : ['Spiteful Druid', 'Murloc Paladin', 'Control Priest', 'Control Warlock'],
    'NoName#13139'       : ['Even Paladin', 'Control Priest', 'Cube Warlock', 'Odd Warrior'],
    'Odemian#2999'       : ['Taunt Druid', 'Control Priest', 'Control Warlock', 'Odd Warrior'],
    'Orange#2309'        : ['Tempo Mage', 'Even Paladin', 'Control Priest', 'Cube Warlock'],
    'RENMEN#2291'        : ['Spiteful Druid', 'Spell Hunter', 'Control Warlock', 'Quest Warrior'],
    'Raena#2283'         : ['Control Priest', 'Shudderwock Shaman', 'Control Warlock', 'Odd Warrior'],
    'Rdu#2340'           : ['Spiteful Druid', 'Tempo Mage', 'Quest Rogue', 'Cube Warlock'],
    'Rikitikitavi#2184'  : ['Spiteful Druid', 'Big Spell Mage', 'Cube Warlock', 'Quest Warrior'],
    'Ronnie#2895'        : ['Spiteful Druid', 'Tempo Mage', 'Control Warlock', 'Odd Warrior'],
    'SCACC#2315'         : ['Taunt Druid', 'Control Priest', 'Quest Rogue', 'Cube Warlock'],
    'Scruffy#2659'       : ['Taunt Druid', 'Control Priest', 'Control Warlock', 'Odd Warrior'],
    'Seiko#2721'         : ['Spiteful Druid', 'Murloc Paladin', 'Control Priest', 'Control Warlock'],
    'ShtanUdachi#2202'   : ['Spiteful Druid', 'Spell Hunter', 'Control Warlock', 'Quest Warrior'],
    'Sintolol#2775'      : ['Spiteful Druid', 'Murloc Paladin', 'Control Priest', 'Control Warlock'],
    'SpaDj#2732'         : ['Taunt Druid', 'Even Paladin', 'Control Priest', 'Cube Warlock'],
    'Springy#2781'       : ['Spiteful Druid', 'Big Spell Mage', 'Even Paladin', 'Cube Warlock'],
    'Swidz#2563'         : ['Taunt Druid', 'Big Spell Mage', 'Control Warlock', 'Odd Warrior'],
    'Thiddi#2854'        : ['Tempo Mage', 'Even Paladin', 'Combo Priest', 'Cube Warlock'],
    'ThijsNL#2223'       : ['Spiteful Druid', 'Tempo Mage', 'Quest Rogue', 'Cube Warlock'],
    'Trec#2878'          : ['Even Paladin', 'Control Priest', 'Control Warlock', 'Odd Warrior'],
    'Turna#2738'         : ['Tempo Mage', 'Even Paladin', 'Quest Rogue', 'Cube Warlock'],
    'Twink#21785'        : ['Taunt Druid', 'Control Priest', 'Control Warlock', 'Odd Warrior'],
    'Tyler#2449'         : ['Taunt Druid', 'Control Priest', 'Quest Rogue', 'Cube Warlock'],
    'Viper#23812'        : ['Taunt Druid', 'Control Priest', 'Miracle Rogue', 'Cube Warlock'],
    'Warma#2764'         : ['Quest Druid', 'Control Priest', 'Quest Rogue', 'Control Warlock'],
    'Windello#2498'      : ['Taunt Druid', 'Combo Priest', 'Quest Rogue', 'Control Warlock'],
    'Zhym#2678'          : ['Spiteful Druid', 'Even Paladin', 'Control Priest', 'Control Warlock'],
    'Zuhex#21312'        : ['Taunt Druid', 'Control Priest', 'Quest Rogue', 'Cube Warlock'],
    'Zuka#2978'          : ['Taunt Druid', 'Tempo Mage', 'Control Priest', 'Control Warlock'],
    'anduriel#21364'     : ['Spiteful Druid', 'Tempo Mage', 'Quest Rogue', 'Cube Warlock'],
    'bequiet#2179'       : ['Tempo Mage', 'Even Paladin', 'Quest Rogue', 'Cube Warlock'],
    'dawido#2832'        : ['Spiteful Druid', 'Murloc Paladin', 'Control Priest', 'Control Warlock'],
    'eilic#2496'         : ['Taunt Druid', 'Control Priest', 'Control Warlock', 'Quest Warrior'],
    'esteban#2504'       : ['Quest Druid', 'Control Priest', 'Quest Rogue', 'Cube Warlock'],
    'fenomeno#21327'     : ['Spiteful Druid', 'Tempo Mage', 'Even Paladin', 'Cube Warlock'],
    'greensheep#2290'    : ['Odd Hunter', 'Tempo Mage', 'Murloc Paladin', 'Odd Rogue'],
    'hunterace#2217'     : ['Taunt Druid', 'Even Paladin', 'Control Priest', 'Control Warlock'],
    'iNS4NE#21840'       : ['Spiteful Druid', 'Control Priest', 'Quest Rogue', 'Cube Warlock'],
    'ignite#21733'       : ['Taunt Druid', 'Big Spell Mage', 'Quest Rogue', 'Control Warlock'],
    'kolmari#2701'       : ['Spiteful Druid', 'Even Paladin', 'Cube Warlock', 'Odd Warrior'],
    'martim#2226'        : ['Spiteful Druid', 'Control Priest', 'Quest Rogue', 'Control Warlock'],
    'ntR#1799'           : ['Taunt Druid', 'Even Paladin', 'Control Priest', 'Control Warlock'],
    'pokrovac#2638'      : ['Spiteful Druid', 'Control Priest', 'Quest Rogue', 'Control Warlock'],
    'riku97#2895'        : ['Taunt Druid', 'Control Priest', 'Quest Rogue', 'Control Warlock'],
    'tanaka#21918'       : ['Taunt Druid', 'Spell Hunter', 'Big Spell Mage', 'Cube Warlock'],
    'xBlyzes#2682'       : ['Spiteful Druid', 'Even Paladin', 'Control Priest', 'Control Warlock'],
    'yogg#2768'          : ['Taunt Druid', 'Combo Priest', 'Quest Rogue', 'Control Warlock'],
    'zumpp#2702'         : ['Even Paladin', 'Control Priest', 'Control Warlock', 'Quest Warrior'],
}

decks_na = {
    #'TEST_1'                  : "Spiteful Druid,Murloc Paladin,Odd Rogue,Cube Warlock".split(','),
    'Alan870806#1754'         : ['Spiteful Druid','Spell Hunter','Miracle Rogue','Cube Warlock'],
    'amnesiac#11705'          : ['Spiteful Druid','Murloc Paladin','Odd Rogue','Control Warlock'],
    'AnguiStar#1109'          : ['Spiteful Druid','Tempo Mage','Even Paladin','Cube Warlock'],
    'Ant#1974'                : ['Spiteful Druid','Tempo Mage','Even Paladin','Cube Warlock'],
    'Apxvoid#11872'           : ['Spiteful Druid','Tempo Mage','Even Paladin','Cube Warlock'],
    'bloodyface#1414'         : ['Spiteful Druid','Even Paladin','Odd Rogue','Cube Warlock'],
    'chosenone#1133'          : ['Spiteful Druid','Tempo Mage','Even Paladin','Cube Warlock'],
    'cthulukitty#1446'        : ['Spiteful Druid','Tempo Mage','Quest Rogue','Cube Warlock'],
    #'Deathsie#1201'           : ['Spiteful Druid','Even Paladin','Spiteful Priest','Control Warlock'],
    'Deathsie#1201'           : ['Spiteful Druid','Even Paladin','Spiteful Druid','Control Warlock'],
    'docpwn#1485'             : ['Spiteful Druid','Tempo Mage','Murloc Paladin','Quest Rogue'],
    'dog#1593'                : ['Spiteful Druid','Control Priest','Control Warlock','Odd Warrior'],
    'DrJikininki#1889'        : ['Spiteful Druid','Tempo Mage','Murloc Paladin','Cube Warlock'],
    'ETC#11729'               : ['Even Paladin','Control Priest','Quest Rogue','Control Warlock'],
    #'fibonacci#1545'          : ['Spell Hunter','Control Priest','Control Warlock','Recruit Warrior'],
    #'fr0zen#1184'             : ['Spell Hunter','Control Priest','Control Warlock','Recruit Warrior'],
    'fibonacci#1545'          : ['Spell Hunter','Control Priest','Control Warlock','Odd Warrior'],
    'fr0zen#1184'             : ['Spell Hunter','Control Priest','Control Warlock','Odd Warrior'],
    'Gallon#11212'            : ['Spiteful Druid','Tempo Mage','Even Paladin','Control Priest'],
    'garifar#1898'            : ['Odd Hunter','Tempo Mage','Murloc Paladin','Odd Rogue'],
    'Gladen#11397'            : ['Spiteful Druid','Tempo Mage','Quest Rogue','Cube Warlock'],
    'Greed#12707'             : ['Spiteful Druid','Tempo Mage','Even Paladin','Cube Warlock'],
    'Guiyze#1681'             : ['Even Paladin','Odd Rogue','Even Shaman','Zoo Warlock'],
    'Houdinii#1378'           : ['Spiteful Druid','Tempo Mage','Even Paladin','Cube Warlock'],
    'IrvinG#1619'             : ['Spiteful Druid','Even Paladin','Control Priest','Cube Warlock'],
    'Joaquin#1259'            : ['Tempo Mage','Even Paladin','Quest Rogue','Cube Warlock'],
    'Justine#1262'            : ['Spiteful Druid','Tempo Mage','Control Priest','Control Warlock'],
    'justsaiyan#1493'         : ['Spiteful Druid','Even Paladin','Odd Rogue','Control Warlock'],
    'killinallday#1537'       : ['Spiteful Druid','Even Paladin','Quest Rogue','Cube Warlock'],
    'klei#11805'              : ['Spiteful Druid','Even Paladin','Control Priest','Control Warlock'],
    'korextron#1532'          : ['Spiteful Druid','Even Paladin','Control Priest','Control Warlock'],
    'lnguagehackr#1412'       : ['Big Spell Mage','Control Priest','Control Warlock','Odd Warrior'],
    'Lucas#12819'             : ['Spiteful Druid','Tempo Mage','Quest Rogue','Cube Warlock'],
    'magkey#1730'             : ['Big Spell Mage','Even Paladin','Control Priest','Cube Warlock'],
    'maxtheripper#1454'       : ['Spiteful Druid','Tempo Mage','Murloc Paladin','Cube Warlock'],
    'Monsanto#1657'           : ['Spiteful Druid','Control Priest','Quest Rogue','Cube Warlock'],
    #'muzzy#1105'              : ['Token Druid','Even Paladin','Odd Rogue','Cube Warlock'],
    'muzzy#1105'              : ['Spiteful Druid','Even Paladin','Odd Rogue','Cube Warlock'],
    'N0lan#11919'             : ['Taunt Druid','Even Paladin','Control Priest','Control Warlock'],
    'Nalguidan#1733'          : ['Spiteful Druid','Even Paladin','Quest Rogue','Cube Warlock'],
    'noblord#1509'            : ['Spiteful Druid','Even Paladin','Odd Rogue','Control Warlock'],
    'PapaJason#1186'          : ['Spiteful Druid','Even Paladin','Odd Rogue','Cube Warlock'],
    'Perna#1691'              : ['Spiteful Druid','Even Paladin','Quest Rogue','Cube Warlock'],
    'Pinche#11361'            : ['Odd Hunter','Tempo Mage','Even Paladin','Odd Rogue'],
    'Pizza#1279'              : ['Spiteful Druid','Tempo Mage','Even Paladin','Cube Warlock'],
    'Pksnow#1547'             : ['Spiteful Druid','Even Paladin','Miracle Rogue','Control Warlock'],
    'PNC#1102'                : ['Spiteful Druid','Even Paladin','Quest Rogue','Cube Warlock'],
    'Purple#1567'             : ['Spiteful Druid','Tempo Mage','Even Paladin','Control Priest'],
    'Quiros2211#1746'         : ['Taunt Druid','Control Priest','Quest Rogue','Cube Warlock'],
    'Rase#1355'               : ['Spiteful Druid','Even Paladin','Quest Rogue','Cube Warlock'],
    'rayC#11391'              : ['Spiteful Druid','Tempo Mage','Murloc Paladin','Cube Warlock'],
    'RealTerror#1827'         : ['Taunt Druid','Control Priest','Control Warlock','Odd Warrior'],
    'Ryuuzu#1203'             : ['Taunt Druid','Control Priest','Quest Rogue','Control Warlock'],
    'Hades#14851'             : ['Spiteful Druid','Murloc Paladin','Odd Rogue','Control Warlock'],
    'seiger#1577'             : ['Even Paladin','Control Priest','Quest Rogue','Cube Warlock'],
    'seohyun628#1679'         : ['Taunt Druid','Control Priest','Control Warlock','Odd Warrior'],
    'SilentStorm#13722'       : ['Spiteful Druid','Tempo Mage','Even Paladin','Cube Warlock'],
    'Sneakyche#1872'          : ['Spiteful Druid','Tempo Mage','Even Paladin','Cube Warlock'],
    'SnipedAgain#1736'        : ['Taunt Druid','Murloc Paladin','Control Priest','Control Warlock'],
    'strifecro#1914'          : ['Spiteful Druid','Tempo Mage','Even Paladin','Odd Rogue'],
    'SwaggyG#1193'            : ['Even Paladin','Odd Rogue','Even Shaman','Zoo Warlock'],
    'T4COTASTIC#1121'         : ['Taunt Druid','Even Paladin','Control Priest','Cube Warlock'],
    'Tarei#11497'             : ['Spiteful Druid','Even Paladin','Quest Rogue','Cube Warlock'],
    'Terrencem#1843'          : ['Even Paladin','Odd Rogue','Even Shaman','Cube Warlock'],
    'TheJordude#1239'         : ['Taunt Druid','Spell Hunter','Control Warlock','Odd Warrior'],
    'TheMaverick#1720'        : ['Tempo Mage','Even Paladin','Control Priest','Control Warlock'],
    'Tuliowz#1870'            : ['Spiteful Druid','Tempo Mage','Even Paladin','Cube Warlock'],
    'UchihaSaske#11453'       : ['Taunt Druid','Control Priest','Control Warlock','Odd Warrior'],
    'ute1234#1252'            : ['Spiteful Druid','Tempo Mage','Murloc Paladin','Cube Warlock'],
    'villain#1999'            : ['Spiteful Druid','Control Priest','Quest Rogue','Cube Warlock'],
    'wabeka#1626'             : ['Spiteful Druid','Even Paladin','Odd Rogue','Cube Warlock'],
    'wiz#11841'               : ['Spiteful Druid','Tempo Mage','Quest Rogue','Cube Warlock'],
    'XisBau5e#1825'           : ['Spiteful Druid','Tempo Mage','Even Paladin','Cube Warlock'],
    'yinus#1258'              : ['Taunt Druid','Even Paladin','Quest Rogue','Cube Warlock'],
    #'yoitsflo#1202'           : ['Token Druid','Even Paladin','Odd Rogue','Cube Warlock'],
    'yoitsflo#1202'           : ['Spiteful Druid','Even Paladin','Odd Rogue','Cube Warlock'],
    'zalae#1766'              : ['Spiteful Druid','Tempo Mage','Even Paladin','Control Priest'],
    'zlsjs#1181'              : ['Spiteful Druid','Control Priest','Quest Rogue','Cube Warlock'],
}
decks = decks_na

win_pcts, num_games, game_count, archetypes, overall_wr = get_win_pcts(min_game_threshold=0, min_game_count=0,limitTop=100)
overrides = [
    ('Zoo Warlock', 'Even Paladin', .47),
    ('Zoo Warlock', 'Tempo Mage', .55),
    ('Zoo Warlock', 'Odd Rogue', .42),
    ('Zoo Warlock', 'Spiteful Druid', .50),
    ('Zoo Warlock', 'Cube Warlock', .30),
    ('Zoo Warlock', 'Control Warlock', .30),
    ('Zoo Warlock', 'Quest Rogue', .65),
    ('Zoo Warlock', 'Control Priest', .43),
    ('Zoo Warlock', 'Murloc Paladin', .50),
    ('Zoo Warlock', 'Taunt Druid', .55),
    ('Zoo Warlock', 'Odd Warrior', .50),
    ('Zoo Warlock', 'Miracle Rogue', .55),
    ('Zoo Warlock', 'Spell Hunter', .43),
    ('Zoo Warlock', 'Even Shaman', .47),
    ('Zoo Warlock', 'Quest Warrior', .45),
    ('Zoo Warlock', 'Quest Druid', .65),
    ('Zoo Warlock', 'Zoo Warlock', .50),
    ('Even Shaman', 'Tempo Mage', .70),
    ('Even Shaman', 'Quest Rogue', .60),
    ('Even Shaman', 'Murloc Paladin', .62),

    ('Control Priest', 'Quest Rogue', .42),
    ('Control Priest', 'Spiteful Druid', .40),
    ('Tempo Mage', 'Quest Rogue', 0.63),
    ('Even Paladin', 'Quest Rogue', 0.63),
            ]
win_pcts = override_wr(overrides,win_pcts)

tops = {}

threshold = 0.60
inverse = 1 - threshold
upsets = 0
total = 0
expected_score = {}
total_wr = 0.0
scores = {}
games = {}
for p1, p2, s1, s2 in round1 + round2 + round3 + round4 + round5 + round6 + round7:
    if p1 not in scores: 
        scores[p1] = 0
        games[p1] = 0
    if p2 not in scores: 
        scores[p2] = 0
        games[p2] = 0
    games[p1] += 1
    games[p2] += 1
    if s1 > s2: scores[p1] += 1
    if s2 > s1: scores[p2] += 1
    wr = calculate_win_rate(decks[p1], decks[p2], win_pcts)
    expected_score[p1] = expected_score.get(p1, 0) + wr
    expected_score[p2] = expected_score.get(p2, 0) + (1-wr)
    if wr > threshold and s1 < s2 or wr < inverse and s1 > s2:
        total_wr += max(wr, 1 - wr)
        print("UPSET:   ", wr, p1, p2, wr, s1, s2)
        upsets += 1
        total += 1
    elif wr > threshold or wr < inverse:
        total_wr += max(wr, 1-wr)
        print("NO UPSET:", wr, p1, p2, wr, s1, s2)
        total += 1
print(upsets, total, total - upsets, round(float(total - upsets) / total * 100, 1))
print(total_wr / total)

#for p1, p2, s1, s2 in round1 + round2 + round3 + round4 + round5 + round6:
#    wr = calculate_win_rate(decks[p1], decks[p2], win_pcts)
#    if (wr > threshold and wr < threshold + 0.05 and s1 < s2) or (wr < inverse and wr > inverse - 0.05 and s1 > s2):
#        print(wr, p1, p2, wr, s1, s2, "UPSET")
#        upsets += 1
#        total += 1
#    elif (wr > threshold and wr < threshold + 0.05) or (wr < inverse and wr > inverse - 0.05):
#        print(wr, p1, p2, wr, s1, s2, "")
#        total += 1
#print(upsets, total, total - upsets, round(float(total - upsets) / total * 100, 1))

#for i, j in sorted(expected_score.items(), key=lambda x:x[1], reverse=True):
#    print(round(j,1),i)
#for i,j in scores.items():
#    print(i, j, round(expected_score.get(i),1), round(j - expected_score.get(i), 1), decks[i])

#for i,j in round6_standings[:16]:
#    print('"' + ",".join(decks[i]) + '"')
pre_tournament_eu = {
    'Rdu#2340' :              3.9,
    'ThijsNL#2223' :          3.9,
    'Hypno#22145' :           3.9,
    'anduriel#21364' :        3.9,
    'Leta#21458' :            3.9,
    'Tyler#2449' :            3.9,
    'Zuhex#21312' :           3.9,
    'Mryagut#2306' :          3.9,
    'SCACC#2315' :            3.9,
    'esteban#2504' :          3.8,
    'Meati#2841' :            3.7,
    'iNS4NE#21840' :          3.7,
    'Bunnyhoppor#2897' :      3.7,
    'Casie#2884' :            3.7,
    'kolmari#2701' :          3.7,
    'BoarControl#2986' :      3.7,
    'fenomeno#21327' :        3.7,
    'bequiet#2179' :          3.7,
    'Viper#23812' :           3.7,
    'Turna#2738' :            3.7,
    'Thiddi#2854' :           3.7,
    'Rikitikitavi#2184' :     3.7,
    'Springy#2781' :          3.6,
    'Kalaxz#2721' :           3.6,
    'Windello#2498' :         3.6,
    'yogg#2768' :             3.6,
    'Babon#21904' :           3.6,
    'Bozzzton#2511' :         3.5,
    'Juristis#2130' :         3.5,
    'greensheep#2290' :       3.5,
    'riku97#2895' :           3.6,
    'Maur1#2225' :            3.6,
    'ignite#21733' :          3.6,
    'ElMachico#2287' :        3.5,
    'Crane333#2314' :         3.5,
    'SpaDj#2732' :            3.5,
    'eilic#2496' :            3.5,
    'Findan#2596' :           3.5,
    'Warma#2764' :            3.5,
    'pokrovac#2638' :         3.5,
    'martim#2226' :           3.5,
    'tanaka#21918' :          3.5,
    'MM78#2809' :             3.5,
    'NoName#13139' :          3.5,
    'Odemian#2999' :          3.5,
    'Orange#2309' :           3.4,
    'Maverick#2233' :         3.5,
    'Twink#21785' :           3.5,
    'Swidz#2563' :            3.5,
    'Scruffy#2659' :          3.5,
    'RENMEN#2291' :           3.4,
    'Seiko#2721' :            3.4,
    'Sintolol#2775' :         3.4,
    'ShtanUdachi#2202' :      3.4,
    'A83650#2106' :           3.4,
    'Nicslay#2567' :          3.4,
    'dawido#2832' :           3.4,
    'Zuka#2978' :             3.4,
    'Kolento#2266' :          3.4,
    'xBlyzes#2682' :          3.3,
    'Glaser#2196' :           3.3,
    'Ronnie#2895' :           3.3,
    'Zhym#2678' :             3.3,
    'Kalas#2638' :            3.3,
    'Trec#2878' :             3.3,
    'ntR#1799' :              3.3,
    'hunterace#2217' :        3.3,
    'Faeli#2572' :            3.3,
    'Jarla#21553' :           3.3,
    'zumpp#2702' :            3.3,
    'Fox#29320' :             3.3,
    'Duarte#21328' :          3.3,
    'Raena#2283' :            3.3,
}

pre_tournament = {
    'Guiyze#1681'          : 3.8,
    'SwaggyG#1193'         : 3.8,
    'bloodyface#1414'      : 3.7,
    'Terrencem#1843'       : 3.7,
    'PapaJason#1186'       : 3.7,
    'fibonacci#1545'       : 3.7,
    'yoitsflo#1202'        : 3.7,
    'fr0zen#1184'          : 3.7,
    'muzzy#1105'           : 3.7,
    'Deathsie#1201'        : 3.7,
    'wabeka#1626'          : 3.7,
    'killinallday#1537'    : 3.6,
    'lnguagehackr#1412'    : 3.6,
    'Nalguidan#1733'       : 3.6,
    'Perna#1691'           : 3.6,
    'Tarei#11497'          : 3.6,
    'UchihaSaske#11453'    : 3.7,
    'Rase#1355'            : 3.6,
    'seohyun628#1679'      : 3.6,
    'PNC#1102'             : 3.6,
    'RealTerror#1827'      : 3.6,
    'dog#1593'             : 3.6,
    'klei#11805'           : 3.6,
    'korextron#1532'       : 3.6,
    'IrvinG#1619'          : 3.6,
    'strifecro#1914'       : 3.6,
    'T4COTASTIC#1121'      : 3.6,
    'Quiros2211#1746'      : 3.6,
    'N0lan#11919'          : 3.5,
    'TheJordude#1239'      : 3.5,
    'docpwn#1485'          : 3.5,
    'rayC#11391'           : 3.5,
    'ute1234#1252'         : 3.5,
    'maxtheripper#1454'    : 3.5,
    'villain#1999'         : 3.5,
    'zlsjs#1181'           : 3.5,
    'Pizza#1279'           : 3.5,
    'Monsanto#1657'        : 3.5,
    'Greed#12707'          : 3.5,
    'DrJikininki#1889'     : 3.5,
    'Houdinii#1378'        : 3.5,
    'SilentStorm#13722'    : 3.5,
    'Tuliowz#1870'         : 3.5,
    'chosenone#1133'       : 3.5,
    'noblord#1509'         : 3.5,
    'seiger#1577'          : 3.5,
    'Sneakyche#1872'       : 3.5,
    'Apxvoid#11872'        : 3.5,
    'AnguiStar#1109'       : 3.5,
    'XisBau5e#1825'        : 3.5,
    'justsaiyan#1493'      : 3.5,
    'magkey#1730'          : 3.5,
    'Hades#14851'          : 3.5,
    'Ant#1974'             : 3.5,
    'amnesiac#11705'       : 3.5,
    'SnipedAgain#1736'     : 3.5,
    'Lucas#12819'          : 3.5,
    'Gladen#11397'         : 3.5,
    'ETC#11729'            : 3.5,
    'yinus#1258'           : 3.5,
    'wiz#11841'            : 3.5,
    'garifar#1898'         : 3.5,
    'cthulukitty#1446'     : 3.5,
    'Ryuuzu#1203'          : 3.4,
    'Gallon#11212'         : 3.4,
    'zalae#1766'           : 3.4,
    'Purple#1567'          : 3.4,
    'Joaquin#1259'         : 3.4,
    'Pinche#11361'         : 3.4,
    'Pksnow#1547'          : 3.4,
    'TheMaverick#1720'     : 3.4,
    'Alan870806#1754'      : 3.3,
    'Justine#1262'         : 3.3,
}
#for p in expected_score.keys():
#    practice = float(expected_score[p]) / games[p]
#    pre = pre_tournament[p] / 7.
#    calc = round(practice / pre, 4)
#    print(p, calc, round(practice, 2))
