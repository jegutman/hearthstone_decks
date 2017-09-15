from hslog import LogParser
 
import pprint
pp = pprint.PrettyPrinter(depth=6)
pp = pp.pprint
 
import tailer
 
from hearthstone.enums import (
    CardType, ChoiceType, GameTag, OptionType, PlayReq, PlayState, PowerType,
    State, Step, Zone
)
 
# for line in tailer.follow(open('/home/dee/.PlayOnLinux/wineprefix/hs/drive_c/Program Files/Hearthstone/Logs/Power.log'), 0):
#     print(line)
global p, g, fplayer, eplayer
p = LogParser()
 
def reload():
    global p, g, fplayer, eplayer
    #with open('/home/dee/.PlayOnLinux/wineprefix/hs/drive_c/Program Files/Hearthstone/Logs/Power.log') as f:
    with open('Power.log') as f:
        p.read(f)
        p.flush()
        g = p.games[-1].export().game
        fplayer = g.players[0].name
        eplayer = g.players[1].name
 
 
 
def get_amount_handcards():
    return len([e for e in g.entities if(e.zone == Zone.HAND
                                         and str(e.controller) == fplayer)])
 
def get_amount_minions(player):
    return len([e for e in g.entities if(e.zone == Zone.PLAY and
                                         e.type == CardType.MINION and
                                         str(e.controller) == player)])
 
def get_heropower_active(player):
    for e in g.entities:
        if(e.zone == Zone.PLAY and e.type == CardType.HERO_POWER and str(e.controller) == player):
            return True if e.tags[GameTag.EXHAUSTED] == 0 else False
 
 
reload()
print("HandCards {:<20}: {}".format("", get_amount_handcards()))
print("Minios {:<20}: {}".format(fplayer, get_amount_minions(fplayer)))
print("Minios {:<20}: {}".format(eplayer, get_amount_minions(eplayer)))
print("HeroPower {:<20}: {}".format(fplayer, get_heropower_active(fplayer)))
print("HeroPower {:<20}: {}".format(eplayer, get_heropower_active(eplayer)))
