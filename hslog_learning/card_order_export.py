from __future__ import print_function
from hearthstone.entities import Card, Game, Player
#from hearthstone.enums import GameTag, Zone
from hslog.export import BaseExporter, EntityTreeExporter
from hearthstone.enums import (
    CardType, ChoiceType, GameTag, OptionType, PlayReq, PlayState, PowerType,
    State, Step, Zone
)
import pprint
pp = pprint.PrettyPrinter(depth=6)
pp = pp.pprint

from json_cards_to_python import *

class CardOrderExporter(BaseExporter):
    game_class = Game
    player_class = Player
    card_class = Card
    player_hands = {}
    last_known_position = {}
    hand_positions = {}
    last_mmm = []

    class EntityNotFound(Exception):
        pass

    def update_packet_tree(self, packet_tree):
        self.packet_tree = packet_tree

    def find_entity(self, entity_id, opcode=""):
        try:
            entity = self.game.find_entity_by_id(entity_id)
        except MissingPlayerData as e:
            raise self.EntityNotFound("Error getting entity %r for %s" % (entity_id, opcode))
        if not entity:
            raise self.EntityNotFound("Attempting %s on entity %r (not found)" % (opcode, entity_id))
        return entity

    def handle_create_game(self, packet):
        self.game = self.game_class(packet.entity)
        self.game.create(packet.tags)
        for player in packet.players:
            self.export_packet(player)
            self.player_hands[player.name] = []
            self.hand_positions[player.name] = {}
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
        entity = self.find_entity(packet.entity, "TAG_CHANGE")
        entity.tag_change(packet.tag, packet.value)
        return entity

    def update_hand(self, block):
        for player in self.player_hands:
            cards_in_hand = [e for e in self.game.entities if(e.zone == Zone.HAND and str(e.controller) == player)]
            self.player_hands[player] = [c for c in self.player_hands if c in cards_in_hand]
            for card in cards_in_hand:
                if card not in self.player_hands[player]:
                    self.player_hands[player].append(card)
            self.player_hands[player].sort(key = lambda x:self.last_known_position.get(x, 11))
            if player == 'MegaManMusic' and self.player_hands[player] != self.last_mmm:
                #print([lookup_card_name(x) for x in self.player_hands[player]])
                self.print_hand('MegaManMusic')
                self.last_mmm = self.player_hands[player][:]

    def get_graveyard_minions(self, player):
        res = []
        for entity in self.game.entities:
            if entity.zone == Zone.GRAVEYARD and entity.type == CardType.MINION:
                if str(entity.controller) == player:
                    res.append(entity)
        return res

    def print_card_list(self, card_list):
        for card in card_list:
            print(lookup_card_name(card))

    def alt_update_hand(self, packet, entity):
        if entity.zone != Zone.HAND:
            return
        player = entity.controller.name
        if packet.value == 0:
            if self.hand_positions[player].get(packet.entity, False):
                self.hand_positions[player].pop(packet.entity)
        else:
            self.hand_positions[player][packet.entity] = packet.value

    def print_hand(self, player):
        cards = sorted(self.hand_positions[player].keys(), key=lambda x:self.hand_positions[player][x])
        print("\n    %-25s" % "Card")
        for position, card in enumerate(cards):
            entity = self.find_entity(card)
            creator = entity.tags.get(GameTag.CREATOR, "")
            if creator != 1:
                creator_entity = self.find_entity(creator) if creator else ""
                creator_name = 'created_by: ' + lookup_card_name(creator_entity) if creator else ""
            print("%-3s" % (position+1), "%-25s" % lookup_card_name(entity), "%-25s" % creator_name)
        #pp([lookup_card_name(self.find_entity(card)) for card in cards])
        

    def handle_block(self, block):
        for p in block.packets:
            self.export_packet(p)
            if 'tag' not in dir(p): continue
            entity = self.find_entity(p.entity, "HANDLE_BLOCK")
            if p.tag == GameTag.ZONE_POSITION:
                self.last_known_position[entity] = p.value
                if 'card_id' in dir(entity):
                    if entity.zone == Zone.HAND:
                        self.alt_update_hand(p, entity)
        self.update_hand(block)

    def handle_metadata(self, packet):
        pass

    def handle_choices(self, packet):
        pass

    def handle_send_choices(self, packet):
        pass

    def handle_chosen_entities(self, packet):
        pass

    def handle_options(self, packet):
        pass

    def handle_option(self, packet):
        pass

    def handle_send_option(self, packet):
        pass

