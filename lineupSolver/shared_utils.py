def win_rates_grid(decks_a, decks_b, win_pcts):
    top_line = "%-20s" % ""
    for deck in decks_b:
        top_line += "%-20s" % deck
    print top_line
    for deck in decks_a:
        line = "%-20s" % deck
        for deck_b in decks_b:
            line += "%6s              " % round(win_pcts.get((deck, deck_b), 0) * 100, 1)
        print line
