from hslog.export import EntityTreeExporter, FriendlyPlayerExporter
from hslog.packets import TagChange
from hslog import LogParser
#from custom_export import *
from card_order_export import *
import platform
import tailer


parser = LogParser()
#with open("Power.log") as f:

power_logs = "Power.log"
if platform.system() == 'Linux':
    if 'Microsoft' in platform.release():
        power_logs = "/mnt/c/Program Files (x86)/Hearthstone/Logs/Power.log"
if platform.system() == 'Darwin':
    power_logs = "/Applications/Hearthstone/Logs/Power.log"

with open(power_logs) as f:
    parser.read(f)
packet_tree = parser.games[-1]
export = CardOrderExporter(packet_tree)
game = export.export()

#initialized = False
#for line in tailer.follow(open(power_logs), 0):
#    parser.read_line(line)
#    if len(parser.games) > 0:
#        packet_tree = parser.games[-1]
#        if not initialized:
#            export = CardOrderExporter(packet_tree)
#            initialized = True
#        else:
#            export.update_packet_tree(packet_tree)


#for card_id in export.card_sequence:
#    print("NEW ENTITY", card_id)
#    for packet in export.tag_events[card_id]:
#        export.print_entity_event(card_id, packet)

#sequence_played = export.cards_played
#for card_name in sequence_played:
#    print(card_name)
