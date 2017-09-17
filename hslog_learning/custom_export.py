from __future__ import print_function
from hearthstone.entities import Card, Game, Player
#from hearthstone.enums import GameTag, Zone
from hslog.export import BaseExporter
from hearthstone.enums import (
    CardType, ChoiceType, GameTag, OptionType, PlayReq, PlayState, PowerType,
    State, Step, Zone
)

from json_cards_to_python import *

class CardOrderExport(BaseExporter):
    game_class = Game
    player_class = Player
    card_class = Card
    tag_change_count = 0
    tag_events = {}
    card_sequence = []
    cards_played = []
    packet_types = set()
    turn_count = {}
    current_player = ""
    ordered_draw = {}
    ids_to_card = {}
    hand_positions = {}

    class EntityNotFound(Exception):
        pass

    def add_entity_tag_event(self, entity_id, packet):
        if entity_id not in self.tag_events:
            self.tag_events[entity_id] = []
            self.card_sequence.append(entity_id)
        self.tag_events[entity_id].append(packet)
        return len(self.tag_events[entity_id])

    def print_entity_event(self, entity_id, packet):
        entity = self.find_entity(entity_id)
        if entity.card_id:
            card = cards_by_raw_id[entity.card_id]
            card_name = card['name']
        else:
            card, card_name = "", ""
        print('%20s' % entity.controller, ' : ', packet.ts, "Entity: %-5s" % packet.entity, "id: %-5s" % packet.packet_id, packet.power_type, "%-30s" % packet.tag, "%20s" % card_name, packet.value)
        

    def find_entity(self, entity_id, opcode=""):
        try:
            entity = self.game.find_entity_by_id(entity_id)
        except MissingPlayerData as e:
            raise self.EntityNotFound("Error getting entity %r for %s" % (entity_id, opcode))
        if not entity:
            raise self.EntityNotFound("Attempting %s on entity %r (not found)" % (opcode, entity_id))
        return entity

    def lookup_entity(self, entity_id):
        return self.ids_to_card.get(entity_id, {'name' : "Unknown"})
        
    def print_ordered_draw(self, player):
        for entity_id, position in self.ordered_draw[player]:
            card_name = cards_by_raw_id[self.lookup_entity(entity_id)]['name']
            print("%25s" % card_name, position)

    def handle_create_game(self, packet):
        #pass
        self.game = self.game_class(packet.entity)
        self.game.create(packet.tags)
        for player in packet.players:
            self.export_packet(player)
            player_name = player.name
            if player_name not in self.turn_count:
                self.turn_count[player_name] = 0
            if player_name not in self.ordered_draw:
                self.ordered_draw[player_name] = []
            if player_name not in self.hand_positions:
                self.hand_positions[player_name] = {}
        return self.game

    def handle_player(self, packet):
        entity_id = int(packet.entity)
        if hasattr(self.packet_tree, "manager"):
            # If we have a PlayerManager, first we mutate the CreateGame.Player packet.
            # This will have to change if we're ever able to immediately get the names.
            player = self.packet_tree.manager.get_player_by_id(entity_id)
            packet.name = player.name
        entity = self.player_class(entity_id, packet.player_id, packet.hi, packet.lo, packet.name)
        entity.tags = dict(packet.tags)
        self.game.register_entity(entity)
        return entity

    def handle_full_entity(self, packet):
        entity = self.card_class(packet.entity, packet.card_id)
        entity.tags = dict(packet.tags)
        self.game.register_entity(entity)
        return entity

    def handle_hide_entity(self, packet):
        entity = self.find_entity(packet.entity, "HIDE_ENTITY")
        entity.hide()
        return entity

    def handle_show_entity(self, packet):
        entity = self.find_entity(packet.entity, "SHOW_ENTITY")
        entity.reveal(packet.card_id, dict(packet.tags))
        return entity

    def handle_change_entity(self, packet):
        entity = self.find_entity(packet.entity, "CHANGE_ENTITY")
        entity.change(packet.card_id, dict(packet.tags))
        return entity

    def update_card_info(self, packet):
        e = self.game.find_entity_by_id(packet.entity)
        if 'card_id' in dir(e):
            if e.card_id is not None:
                self.ids_to_card[packet.packet_id] = e.card_id

    def check_update_hand(self, packet):
        if packet.tag == GameTag.ZONE_POSITION:
            e = self.game.find_entity_by_id(packet.entity)
            player = e.controller.name
            if player in self.ordered_draw:
                #for i in dir(packet):
                #    print(i, eval('packet.' + i))
                #    assert False
                self.ordered_draw[player].append((packet.packet_id, packet.value))
                if packet.value > 0:
                    self.hand_positions[player][packet.value] = packet.packet_id

    def print_hand(self, player):
        for position in sorted(self.hand_positions[player].keys()):
            print("%2s" % position, end = '')
            print(cards_by_raw_id[self.lookup_entity(self.hand_positions[player][position])]['name'])
            

    def handle_tag_change(self, packet):
        self.check_update_hand(packet)
        self.update_card_info(packet)
        self.packet_types.add(packet.tag)
        #print dir(packet)
        #e = packet.entity
        #e = self.find_entity(packet.entity, "TAG_CHANGE")
        e = self.game.find_entity_by_id(packet.entity)
        if packet.tag == GameTag.CURRENT_PLAYER and packet.value == 1:
            self.current_player = e.controller
            if self.current_player not in self.turn_count: self.turn_count[self.current_player] = 0
        if packet.tag == GameTag.TURN:
            #print("TURN? :", '%20s' % e.controller, ' : ', packet.ts, "Entity: %-5s" % packet.entity, "id: %-5s" % packet.packet_id, packet.power_type, "%-30s" % packet.tag, packet.value)
            self.turn_count[self.current_player] += 1
            self.cards_played.append("\nStart Turn %s %s" % (self.turn_count[self.current_player], self.current_player) )
        if not e.can_be_in_deck:
            if 'card_id' in dir(e):
                card = cards_by_raw_id.get(e.card_id, {'name' : 'no_card'})
                card_name = card['name']
                #print('NON-CARD', '%20s' % e.controller, ' : ', packet.ts, "Entity: %-5s" % packet.entity, "id: %-5s" % packet.packet_id, packet.power_type, "%-30s" % packet.tag, "%20s" % card_name, packet.value)
                if e.card_id in hero_powers and packet.value == 1:
                    self.cards_played.append('Hero Power: ' + card_name)
            return
        #print(e.card_id)
        if e.card_id:
            card = cards_by_raw_id[e.card_id]
            card_name = card['name']
        else:
            card, card_name = "", ""
        #if card_name == 'Holy Smite':
        #    print(dir(e))
        #    print(dir(packet))
        #    assert False
        encounter_num = self.add_entity_tag_event(packet.entity, packet)
        #print("ENCOUNTER: %s" % encounter_num)
        if packet.tag == GameTag.ZONE_POSITION:
            #self.cards_played.append((card, card_name))
            self.cards_played.append(card_name)
            print("ZONE_POSITION %4s" % self.tag_change_count, '%20s' % e.controller, ' : ', packet.ts, "Entity: %-5s" % packet.entity, "id: %-5s" % packet.packet_id, packet.power_type, "%-30s" % packet.tag, "%20s" % card_name, packet.value)
            print("ZONE_POSITION", dir(packet))
            print("ZONE_POSITION", e.zone)
        if packet.tag == GameTag.JUST_PLAYED and packet.value == 1:
            #self.cards_played.append((card, card_name))
            self.cards_played.append(card_name)
            print("JUST_PLAYED %4s" % self.tag_change_count, '%20s' % e.controller, ' : ', packet.ts, "Entity: %-5s" % packet.entity, "id: %-5s" % packet.packet_id, packet.power_type, "%-30s" % packet.tag, "%20s" % card_name, packet.value)
        if encounter_num == 1 or packet.value == Zone.DECK:
            #if isinstance(e, Card): return
            if e.zone != Zone.HAND:
                #print("OPP %4s" % self.tag_change_count, '%20s' % e.controller, ' : ', packet.ts, "Entity: %-5s" % packet.entity, "id: %-5s" % packet.packet_id, packet.power_type, "%-30s" % packet.tag, "%20s" % card_name, packet.value)
                pass
            else:
                #print("    %4s" % self.tag_change_count, '%20s' % e.controller, ' : ', packet.ts, "Entity: %-5s" % packet.entity, "id: %-5s" % packet.packet_id, packet.power_type, "%-30s" % packet.tag, "%20s" % card_name, packet.value)
                pass
            # excluding power_type because always TAG_CHANGE in this method
            self.tag_change_count += 1
            #assert False
            #['entity', 'packet_id', 'power_type', 'tag', 'ts', 'value']
            pass
