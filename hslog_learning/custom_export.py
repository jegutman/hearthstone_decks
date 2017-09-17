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

    def handle_create_game(self, packet):
        #pass
        self.game = self.game_class(packet.entity)
        self.game.create(packet.tags)
        for player in packet.players:
            self.export_packet(player)
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

    def handle_tag_change(self, packet):
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
                print('NON-CARD', '%20s' % e.controller, ' : ', packet.ts, "Entity: %-5s" % packet.entity, "id: %-5s" % packet.packet_id, packet.power_type, "%-30s" % packet.tag, "%20s" % card_name, packet.value)
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
        if packet.tag == GameTag.JUST_PLAYED and packet.value == 1:
            #self.cards_played.append((card, card_name))
            self.cards_played.append(card_name)
            print("JUST_PLAYED %4s" % self.tag_change_count, '%20s' % e.controller, ' : ', packet.ts, "Entity: %-5s" % packet.entity, "id: %-5s" % packet.packet_id, packet.power_type, "%-30s" % packet.tag, "%20s" % card_name, packet.value)
        if encounter_num == 1 or packet.value == Zone.DECK:
            #if isinstance(e, Card): return
            if e.zone != Zone.HAND:
                print("OPP %4s" % self.tag_change_count, '%20s' % e.controller, ' : ', packet.ts, "Entity: %-5s" % packet.entity, "id: %-5s" % packet.packet_id, packet.power_type, "%-30s" % packet.tag, "%20s" % card_name, packet.value)
            else:
                print("    %4s" % self.tag_change_count, '%20s' % e.controller, ' : ', packet.ts, "Entity: %-5s" % packet.entity, "id: %-5s" % packet.packet_id, packet.power_type, "%-30s" % packet.tag, "%20s" % card_name, packet.value)
            # excluding power_type because always TAG_CHANGE in this method
            self.tag_change_count += 1
            #assert False
            #['entity', 'packet_id', 'power_type', 'tag', 'ts', 'value']
            
            pass
            #entity = self.find_entity(packet.entity, "TAG_CHANGE")
            #entity.tag_change(packet.tag, packet.value)
            #return entity