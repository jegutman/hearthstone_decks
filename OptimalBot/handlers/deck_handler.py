from shared_utils import *
from config import *
import re
import sys
from arg_split import get_args
from deck_manager import EasyDeck, print_side_by_side, print_side_by_side_diff, side_by_side_diff_lines

#helpstring = """`Deck:
helpstring = """Deck:
To insert a deck: !deck <deckstring> --name <deck_name> --archetype <archetype>
    (name and archetype flags are optional, but helpful)
To update a deck: !update <deckstring> --name <deck_name> --archetype <archetype>
"""
#`
#"""

#helpstring_search = """`Search:
helpstring_search = """Search:
Flags that can be used for search:
-name
-class
-archetype
-date (format YYYY_MM_DD)
all of these accept .* as a wildcard
"""
#`
#"""

class DeckHandler():
    def __init__(self):
        pass

    def handle(self, args, message, deck_db_handler):
        if 'help' in args.split()[0]:
            return helpstring
        deckstrings, flags = get_args(args)
        if len(deckstrings) == 1:
            deck_code = deckstrings[0]
            deck_name = flags.get('name')
            deck_archetype = flags.get('archetype')
            if not deck_name:
                deck_name = deck_db_handler.get_name_from_code(deck_code)
            deck_db_handler.process_deck(message, deck_code, name=deck_name, archetype=deck_archetype)
            try:
                #return '`' + EasyDeck(deckstrings[0], deck_name).deck_print_lines() + '`'
                return EasyDeck(deckstrings[0], deck_name).deck_print_lines()
            except:
                #return '`%s`' % "Error: Bad deckstring"
                return '%s' % "Error: Bad deckstring"
        else:
            decks = []
            for i in deckstrings:
                deck_name = deck_db_handler.get_name_from_code(i)
                if not deck_name:
                    deck_name = ''
                decks.append(EasyDeck(i, deck_name))
            if not len(set([i.get_class() for i in decks])) == 1:
                #return '`cannot compare decks from different classes`'
                return 'cannot compare decks from different classes'
            try:
                #return '`' + side_by_side_diff_lines(decks) +'`'
                return side_by_side_diff_lines(decks)
            except:
                #return '`%s`' % "Error: Bad deckstring"
                return '%s' % "Error: Bad deckstring"
    
    def handle_update(self, args, message, deck_db_handler):
        deckstrings, flags = get_args(args)
        deck_code = deckstrings[0]
        deck_name = flags.get('name')
        deck_archetype = flags.get('archetype')
        if deck_db_handler.update_deck_label(message, deck_code, name=deck_name, archetype=deck_archetype):
            #return '`SUCCESS`'
            return 'SUCCESS'
        else:
            #return '`UPDATE FAILED`'
            return 'UPDATE FAILED'

    def handle_similar(self, args, message, deck_db_handler):
        deckstrings, flags = get_args(args)
        ds = deckstrings[0]
        if re.match('[0-9]+', ds):
            deck_code, deck_name = deck_db_handler.get_deck_from_id(ds)
            deck = EasyDeck(deck_code, deck_name)
        else:
            deck = EasyDeck(ds)
        deck_class = deck.get_class()
        max_results = flags.get('limit', 5)
        max_dist = flags.get('max_dist', 6)
        to_compare = deck_db_handler.get_decks_by_class(deck_class)
        res = []
        for deck_id, deck_archetype, deck_code in to_compare:
            tmp_deck = EasyDeck(deck_code)
            distance = deck.get_distance(tmp_deck)
            res.append((distance, deck_id, deck_code))
        res_final = sorted([i for i in res if i[0] <= max_dist], key=lambda x:(x[0],-x[1],x[2]))[:max_results]
        if len(res_final) == 0:
            return 'No deck within %(max_dist)s cards of deck' % locals()
        #print_res = '`'
        print_res = ''
        print_res += "%-7s %-7s %-s" % ('deck_id', 'dist', 'deck_code') + '\n'
        for distance, deck_id, deck_code in res_final:
            print_res += "%(deck_id)-7s %(distance)-7s %(deck_code)-s" % locals() + '\n'
        #print_res += '`'
        return print_res

    def handle_search(self, args, message, deck_db_handler, use_playoffs=False):
        deckstrings, flags = get_args(args)
        if 'help' in args.split()[0]:
            return helpstring_search
        if message.channel.name in PRIVATE_CHANNELS or message.server.name in PRIVATE_SERVERS:
            allow_private = True
        else:
            allow_private = False
        return deck_db_handler.search(args,flags, allow_private, message.server.name, use_playoffs=use_playoffs)

    def handle_cup_stats(self, args, message, deck_db_handler):
        player, flags = get_args(args)
        #if 'help' in args.split()[0]:
        #    return helpstring_search
        res = deck_db_handler.get_record(player)
        res_str = ""
        res_str += "%-24s %3s %3s %3s %s\n" % ('player', 'cups', 'W', 'L', 'pct')
        for player, cups, W, G in res[:25]:
            pct = round(W / G * 100, 1)
            L = G - W
            res_str += "%-24s %3s %3s %3s %s\n" % (player, cups, W, L, pct)
        #if len(res) > 10:
        #    res_str += '*Limited to 10 most recent results'
        #res_str += '`'
        return res_str

    def handle_cup_history(self, args, message, deck_db_handler):
        player, flags = get_args(args)
        res = deck_db_handler.get_cup_history(player)
        res_str = ""
        res_str += "%3s %-18s %3s %3s %s\n" % ('cup', 'player', 'W', 'L', 'Archetype')
        totW, totL = 0,0
        for cup, player, arch, W, G in res[-50:]:
            cup = cup.split('-')[-1]
            L = G - W
            totW += W
            totL += L
            res_str += "%3s %-18s %3s %3s %s\n" % (cup, player, W, L, arch)
        pct = round(totW / max((totW + totL), 1) * 100, 1)
        res_str += "%3s %-18s %3s %3s %s\n" % ("TOT", player, totW, totL, pct)
        return res_str

    def handle_cup_meta(self, args, message, deck_db_handler):
        tournaments, flags = get_args(args)
        #if 'help' in args.split()[0]:
        #    return helpstring_search
        res = deck_db_handler.get_meta(tournaments)
        res_str = ""
        res_str += "%-24s %3s\n" % ('Archetype', 'count')
        total = 0
        for arch, count in res[:50]:
            res_str += "%-24s %3s\n" % (arch, count)
            total += int(count)
        #if len(res) > 10:
        #    res_str += '*Limited to 10 most recent results'
        #res_str += '`'
        res_str += "%-24s %3s\n" % ('TOTAL', total)
        return res_str

    def handle_cup_link(self, args, message, deck_db_handler):
        tournament, flags = get_args(args)
        #if 'help' in args.split()[0]:
        #    return helpstring_search
        res = deck_db_handler.get_link(tournament)
        res_str = '%(res)s' % locals()
        return res_str

    def handle_cup_winners(self, args, message, deck_db_handler):
        query_res = deck_db_handler.get_winners()
        res = []
        res_str = ""
        res_str += "%3s %-20s %-20s\n" % ('', 'player', 'arch')
        for tourn, player, arch in query_res[-75:-50]:
            res_str += "%3s %-20s %-20s\n" % (tourn, player, arch)
        res.append(res_str)
        res_str = ""
        for tourn, player, arch in query_res[-50:-25]:
            res_str += "%3s %-20s %-20s\n" % (tourn, player, arch)
        res.append(res_str)
        res_str = ""
        #res_str += "%3s %-20s %-20s\n" % ('', 'player', 'arch')
        for tourn, player, arch in query_res[-25:]:
            res_str += "%3s %-20s %-20s\n" % (tourn, player, arch)
        res.append(res_str)
        #if len(res) > 10:
        #    res_str += '*Limited to 10 most recent results'
        #res_str += '`'
        #return res_str
        return res

    def handle_cup_deck(self, args, message, deck_db_handler):
        query, flags = get_args(args)
        return deck_db_handler.get_cup_deck(query)

    def handle_cup_details(self, args, message, deck_db_handler):
        query, flags = get_args(args)
        res = deck_db_handler.get_cup_details(query)
        count = 0
        res_str = ""
        res_str += "%2s %-20s %-20s %2s %2s %3s %s\n" % ('', 'p1', 'p2', 's1', 's2', 'res', 'opp_arch')
        for round_number, p1, p2, s1, s2, r, opp_arch in res:
            count += 1
            if count != 1 and int(round_number) == 1:
                res_str += ' Top 8\n'
            res_str += "%2s %-20s %-20s %2s %2s %3s %s\n" % (round_number, p1, p2, s1, s2, r, opp_arch)
        return res_str

    def handle_lineup(self, args, message, deck_db_handler, use_playoffs=True):
        deckstrings, flags = get_args(args)
        if 'help' in args.split()[0]:
            return helpstring_search
        if message.channel.name in PRIVATE_CHANNELS:
            allow_private = True
        elif message.server is not None and message.server.name in PRIVATE_SERVERS:
            allow_private = True
        else:
            allow_private = False
        return deck_db_handler.lineup(args,flags, allow_private, message.server.name, use_playoffs=use_playoffs)

    def handle_compare_all(self, args, message, deck_db_handler):
        deckstrings, flags = get_args(args)
        if message.channel.name in PRIVATE_CHANNELS or message.server.name in PRIVATE_SERVERS:
            allow_private = True
        else:
            allow_private = False
        decks = deck_db_handler.search_helper(args,flags, allow_private, message.server.name, limit=6)
        deckstrings_to_compare = [i[-1] for i in decks]
        args = " ".join(deckstrings_to_compare)
        return self.handle(args, message, deck_db_handler)

    def handle_compare(self, args, message, deck_db_handler):
        deckstrings, flags = get_args(args)
        deckstrings_to_compare = []
        for d in deckstrings:
            if re.match('[0-9]+', d):
                deck_code, deck_name = deck_db_handler.get_deck_from_id(d)
                deckstrings_to_compare.append(deck_code)
            else:
                deckstrings_to_compare.append(d)
        args = " ".join(deckstrings_to_compare)
        return self.handle(args, message, deck_db_handler)
