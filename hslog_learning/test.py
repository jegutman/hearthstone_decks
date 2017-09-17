from hslog.export import EntityTreeExporter, FriendlyPlayerExporter
from hslog.packets import TagChange
from hslog import LogParser
from custom_export import *

#def logfile(path):
#    return os.path.join(LOG_DATA_DIR, "hslog-tests", path)

parser = LogParser()
with open("Power.log") as f:
#with open("/Applications/Hearthstone/Logs/Power.log") as f:
    parser.read(f)

packet_tree = parser.games[-1]
#packet_tree = parser.games[-2]
export = CardOrderExport(packet_tree)
game = export.export()

for card_id in export.card_sequence:
    print("NEW ENTITY", card_id)
    for packet in export.tag_events[card_id]:
        export.print_entity_event(card_id, packet)

sequence_played = export.cards_played
for card_name in sequence_played:
    print(card_name)
