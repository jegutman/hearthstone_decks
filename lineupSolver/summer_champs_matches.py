pairings = [
    #Group A
    ('Rase', 'Viper', 2, 3),
    ('XiaoT', 'Tansoku', 3, 1),
    ('Viper', 'XiaoT', 0, 3),
    ('Rase', 'Tansoku', 2, 3),
    ('Viper', 'Tansoku', 3, 2),
    #Group B
    ('A83650', 'BloodTrail', 2, 3),
    ('Nalguidan', 'YuYi', 1, 3),
    ('BloodTrail', 'Nalguidan', 1, 3),
    ('A83650', 'YuYi', 3, 2),
    ('BloodTrail', 'A83650', 3, 1),
    #Group C
    ('Jinsoo', 'Rugal', 3, 1),
    ('Turna', 'Dog', 3, 0),
    ('Jinsoo', 'Turna', 3, 0),
    ('Rugal', 'Dog', 1, 3),
    ('Turna', 'Rugal', 1, 3),
    #Group D
    ('Leaoh', 'killinallday', 1, 3),
    ('Glory', 'Bunnyhoppor', 2, 3),
    ('killinallday', 'Bunnyhoppor', 1, 3),
    ('Leaoh', 'Glory', 0, 3),
    ('killinallday', 'Glory', 1, 3),
    # Top 8
    ('XiaoT', 'A83650', 0, 3),
    ('Jinsoo', 'killinallday', 0, 3),
    ('Viper', 'Nalguidan', 2, 3),
    ('Bunnyhoppor', 'Turna', 3, 2),
    # Top 4
    ('A83650', 'killinallday', 3, 0),
    ('Viper', 'Bunnyhoppor', 2, 3),
    # Finals
    ('A83650', 'Bunnyhoppor', 1, 3),
]

deck_matches = [
    # Rase vs Viper
    ('Big Spell Mage', 'Miracle Rogue', 'L'),
    ('Big Spell Mage', 'Even Warlock', 'W'),
    ('Taunt Druid', 'Big Spell Mage', 'L'),
    ('Even Warlock', 'Even Warlock', 'W'),
    ('Quest Warrior', 'Even Warlock', 'L'),

    # XiaoT vs Tansoku
    ('Recruit Hunter', 'Even Warlock', 'W'),
    ('Spiteful Druid', 'Even Warlock', 'L'),
    ('Spiteful Druid', 'Taunt Druid', 'W'),
    ('Even Warlock', 'Taunt Druid', 'W'),

    # Viper vs XiaoT
    ('Big Spell Mage', 'Even Warlock', 'L'),
    ('Big Spell Mage', 'Spiteful Druid', 'L'),
    ('Big Spell Mage', 'Miracle Rogue', 'L'),

    # Rase vs Tansoku
    ('Shudderwock Shaman', 'Taunt Druid', 'W'),
    ('Taunt Druid', 'Miracle Rogue', 'L'),
    ('Taunt Druid', 'Taunt Druid', 'L'),
    ('Taunt Druid', 'Even Warlock', 'W'),
    ('Quest Warrior', 'Even Warlock', 'L'),

    # Viper vs Tansoku
    ('Big Spell Mage', 'Taunt Druid', 'W'),
    ('Shudderwock Shaman', 'Taunt Druid', 'W'),
    ('Even Warlock', 'Taunt Druid', 'L'),
    ('Even Warlock', 'Even Warlock', 'L'),
    ('Even Warlock', 'Recruit Hunter', 'W'),

    # A83650 vs BloodTrail
    ('Taunt Druid', 'Even Warlock', 'L'),
    ('Cube Warlock', 'Taunt Druid', 'W'),
    ('Taunt Druid', 'Taunt Druid', 'W'),
    ('Control Priest', 'Recruit Hunter', 'L'),
    ('Control Priest', 'Taunt Druid', 'L'),

    # Nalguidan vs YuYi
    ('Recruit Hunter', 'Miracle Rogue', 'L'),
    ('Taunt Druid', 'Miracle Rogue', 'W'),
    ('Shudderwock Shaman', 'Even Warlock', 'W'),
    ('Recruit Hunter', 'Even Warlock', 'W'),

    # BloodTrail vs Nalguidan
    ('Recruit Hunter', 'Taunt Druid', 'W'),
    ('Shudderwock Shaman', 'Taunt Druid', 'L'),
    ('Even Warlock', 'Recruit Hunter', 'L'),
    ('Even Warlock', 'Shudderwock Shaman', 'L'),

    # A83650 vs YuYi
    ('Control Priest', 'Taunt Druid', 'L'),
    ('Control Priest', 'Even Shaman', 'W'),
    ('Miracle Rogue', 'Even Shaman', 'W'),
    ('Taunt Druid', 'Even Shaman', 'L'),
    ('Taunt Druid', 'Even Warlock', 'W'),

    # BloodTrail vs A83650
    ('Recruit Hunter', 'Taunt Druid', 'L'),
    ('Even Warlock', 'Cube Warlock', 'W'),
    ('Recruit Hunter', 'Cube Warlock', 'L'),
    ('Taunt Druid', 'Control Priest', 'L'),

    # Jinsoo vs Rugal
    ('Control Priest', 'Control Priest', 'W'),
    ('Big Spell Mage', 'Control Priest', 'L'),
    ('Big Spell Mage', 'Taunt Druid', 'W'),
    ('Even Warlock', 'Taunt Druid', 'W'),

    # Turna vs Dog
    ('Even Warlock', 'Shudderwock Shaman', 'W'),
    ('Token Druid', 'Combo Priest', 'W'),
    ('Odd Paladin', 'Shudderwock Shaman', 'W'),

    # Jinsoo vs Turna
    ('Control Priest', 'Even Warlock', 'W'),
    ('Big Spell Mage', 'Odd Paladin', 'L'),
    ('Big Spell Mage', 'Even Warlock', 'W'),
    ('Miracle Rogue', 'Even Shaman', 'L'),
    ('Miracle Rogue', 'Even Warlock', 'W'),

    # Rugal vs Dog
    ('Control Priest', 'Taunt Druid', 'L'),
    ('Even Warlock', 'Even Warlock', 'W'),
    ('Control Priest', 'Even Warlock', 'W'),
    ('Taunt Druid', 'Even Warlock', 'W'),

    # Turna vs Rugal
    ('Even Warlock', 'Taunt Druid', 'W'),
    ('Odd Paladin', 'Even Warlock', 'L'),
    ('Odd Paladin', 'Big Spell Mage', 'W'),
    ('Even Shaman', 'Big Spell Mage', 'W'),

    # Leaoh vs Killin
    ('Shudderwock Shaman', 'Even Warlock', 'L'),
    ('Odd Paladin', 'Even Shaman', 'L'),
    ('Shudderwock Shaman', 'Odd Paladin', 'W'),
    ('Odd Paladin', 'Odd Paladin', 'L'),

    # Glory vs Bunnyhoppor
    ('Shudderwock Shaman', 'Big Spell Mage', 'W'),
    ('Cube Warlock', 'Big Spell Mage', 'L'),
    ('Taunt Druid', 'Shudderwock Shaman', 'W'),
    ('Even Warlock', 'Even Warlock', 'L'),
    ('Even Warlock', 'Shudderwock Shaman', 'L'),

    # killin vs bunnyhoppor
    ('Even Shaman', 'Even Warlock', 'L'),
    ('Even Shaman', 'Miracle Rogue', 'W'),
    ('Odd Paladin', 'Miracle Rogue', 'L'),
    ('Even Warlock', 'Shudderwock Shaman', 'L'),

    # Leaoh vs Glory
    ('Shudderwock Shaman', 'Taunt Druid', 'L'),
    ('Cube Warlock', 'Miracle Rogue', 'L'),
    ('Even Warlock', 'Shudderwock Shaman', 'L'),

    # Killin vs Glory
    ('Token Druid', 'Shudderwock Shaman', 'L'),
    ('Even Shaman', 'Miracle Rogue', 'W'),
    ('Token Druid', 'Taunt Druid', 'W'),
    ('Even Warlock', 'Taunt Druid', 'W'),

    # XiaoT vs A83650
    ('Spiteful Druid', 'Cube Warlock', 'L'),
    ('Recruit Hunter', 'Taunt Druid', 'L'),
    ('Spiteful Druid', 'Control Priest', 'L'),

    # Jinsoo vs Killin
    ('Miracle Rogue', 'Odd Paladin', 'L'),
    ('Miracle Rogue', 'Even Warlock', 'L'),
    ('Big Spell Mage', 'Even Shaman', 'L'),

    # Viper vs Nalguidan
    ('Recruit Hunter', 'Even Warlock', 'L'),
    ('Recruit Hunter', 'Shudderwock Shaman', 'W'),
    ('Shudderwock Shaman', 'Shudderwock Shaman', 'W'),
    ('Taunt Druid', 'Miracle Rogue', 'L'),
    ('Taunt Druid', 'Shudderwock Shaman', 'L'),

    # Bunnyhoppor vs Turna
    ('Big Spell Mage', 'Odd Paladin', 'L'),
    ('Big Spell Mage', 'Even Warlock', 'W'),
    ('Shudderwock Shaman', 'Even Shaman', 'L'),
    ('Miracle Rogue', 'Even Warlock', 'W'),
    ('Shudderwock Shaman', 'Even Warlock', 'W'),

    # A83650 vs killin
    ('Miracle Rogue', 'Even Warlock', 'W'),
    ('Taunt Druid', 'Token Druid', 'W'),
    ('Even Warlock', 'Token Druid', 'W'),

    # Viper vs Bunnyhoppor
    ('Miracle Rogue', 'Even Warlock', 'W'),
    ('Shudderwock Shaman', 'Even Warlock', 'W'),
    ('Even Warlock', 'Big Spell Mage', 'L'),
    ('Even Warlock', 'Miracle Rogue', 'L'),
    ('Even Warlock', 'Even Warlock', 'L'),

    # A83650 vs Bunnyhoppor
    ('Control Priest', 'Shudderwock Shaman', 'L'),
    ('Cube Warlock', 'Big Spell Mage', 'W'),
    ('Control Priest', 'Big Spell Mage', 'L'),
    ('Taunt Druid', 'Even Warlock', 'L'),
]

wins = {}
games = {}
for i,j, res in deck_matches:
    if (i,j) not in wins:
        wins[(i,j)] = 0
        games[(i,j)] = 0
        wins[(j,i)] = 0
        games[(j,i)] = 0
    games[(i,j)] += 1
    games[(j,i)] += 1
    if res == 'W':
        wins[(i,j)] += 1
    else:
        wins[(j,i)] += 1
        
for i,g in sorted(games.items(), key=lambda x:x[1], reverse=True):
    i,j = i
    if i>=j: continue
    w = wins[(i,j)]
    pct = round(float(w) / g * 100,1)
    print("%-20s %-20s %s %s %s" % (i,j, w, g, pct))
    
