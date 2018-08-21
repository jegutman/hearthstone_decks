from battlefy_decks_results import *

urls = sys.argv[1:]

player_matches = {}
decks = {}
archetypes = {}
all_matches = []
unlabeled = {}
for url in urls:
    #tmp_decks, tmp_matches, tmp_player_matches = process_battlefy_url(url)
    tmp_decks, tmp_matches, tmp_player_matches = process_battlefy_url(url, only_finished=True)
    # this is not quite right because could be lists to append to
    for i,j in tmp_player_matches.items():
        player_matches[i] = player_matches.get(i, []) + j
    #player_matches.update(tmp_player_matches)
    for i,j in tmp_decks.items():
        if len(j) > len(decks.get(i, [])):
            decks[i] = j
    #decks.update(tmp_decks)
    all_matches += tmp_matches

wins = {}
losses = {}
for x in player_matches.keys():
    total_losses = sum([1-i[4] if i[2] == x else i[4] for i in player_matches[x]])
    total_wins = sum([i[4] if i[2] == x else 1-i[4] for i in player_matches[x]])
    wins[x] = total_wins
    losses[x] = total_losses

for player, lineup in decks.items():
    archetypes[player] = []
    for deck in lineup:
        try:
            tmp = EasyDeck(deck)
        except:
            print(deck)
        label = label_archetype(tmp, threshold=8)
        if label:
            archetypes[player].append(label)
        else:
            #unlabeled.append((deck, tmp.get_class()))
            unlabeled[tmp.get_class()] = unlabeled.get(tmp.get_class(), []) + [deck]
    if wins[player] >= 7:
        print(",".join(sorted(archetypes[player], key=lambda x:x.split(' ')[1])))

for deck_class in unlabeled:
    for i in unlabeled[deck_class]: print(i)
    for i in print_side_by_side([EasyDeck(j) for j in unlabeled[deck_class]], sort_decks=True): print(i)

def print_archetypes(archetypes):
    for i,j in archetypes.items():
        if len(j) == 3: 
            print('        "' + ",".join(j) + '",')

