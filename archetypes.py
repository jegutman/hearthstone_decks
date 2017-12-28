def get_archetypes_by_class(decks_by_class):
    archetypes = {}
    uncategorized_by_class = {}
    for deck_class in decks_by_class:
        uncategorized_by_class[deck_class] = []
        cat_distance = 7
        new_distance = 9
        archetypes[deck_class] = []
        uncategorized = []
        for deck in decks_by_class[deck_class]:
            if len(archetypes[deck_class]) == 0:
                archetypes[deck_class].append([deck])
                continue
            categorized = False
            mds = []
            for at in archetypes[deck_class]:
                min_distance = min([deck.get_distance(d) for d in at])
                mds.append(min_distance)
                if min_distance <= cat_distance:
                    at.append(deck)
                    break
            if min(mds) >= new_distance:
                archetypes[deck_class].append([deck])
            elif min(mds) > cat_distance:
                uncategorized.append((min(mds), deck))
        removed = uncategorized
        pass_through = 1
        while len(removed) > 0:
            #print len(removed)
            pass_through += 1
            removed = []
            for min_md, deck in uncategorized:
                for at in archetypes[deck_class]:
                    min_distance = min([deck.get_distance(d) for d in at])
                    mds.append(min_distance)
                    if min_distance <= cat_distance:
                        at.append(deck)
                        removed.append(deck)
                        #print str(pass_through) + "pass categorization", deck
                        break
            uncategorized = [d for d in uncategorized if d[1] not in removed]
        # keep adding highest distance deck once and repeat
        while len(uncategorized) > 0:
            to_append = max(uncategorized)
            archetypes[deck_class].append([to_append[1]])
            uncategorized.remove(to_append)
            removed = uncategorized
            while len(removed) > 0:
                #print len(removed)
                pass_through += 1
                removed = []
                for min_md, deck in uncategorized:
                    for at in archetypes[deck_class]:
                        min_distance = min([deck.get_distance(d) for d in at])
                        mds.append(min_distance)
                        if min_distance <= cat_distance:
                            at.append(deck)
                            removed.append(deck)
                            #print str(pass_through) + "pass categorization", deck
                            break
                uncategorized = [d for d in uncategorized if d[1] not in removed]

        uncategorized_by_class[deck_class] = uncategorized
    return archetypes
