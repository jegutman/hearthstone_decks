lineups = [
    ('KGo',                 'Secret Mage,Highlander Priest,Murloc Paladin'),
    ('TheJordude',          'Secret Mage,Big Priest,Tempo Rogue'),
    ('Zapgaze',             'Tempo Priest,Tempo Rogue,Zoo Warlock'),
    ('Mansion',             'Secret Mage,Token Shaman,Highlander Priest'),
    ('Fwan',                'Quest Rogue,Quest Druid,Highlander Priest'),
    ('Ginky',               'Highlander Priest,Tempo Rogue,Zoo Warlock'),
    ('Apxvoid',             'Highlander Priest,Secret Mage,Zoo Warlock'),
    ('XisBau5e',            'Highlander Priest,Jade Druid,Spell Hunter'),
    ('MartinRiendeau',      'Aggro Paladin,Big Druid,Big Priest'),
    ('The Jiminator',       'Tempo Rogue,Highlander Warlock,Highlander Priest'),
    ('BigBlackDeck',        'Pirate Warrior,Demon Warlock,Dragon Priest'),
    ('Luffy',               'Demon Warlock,Highlander Priest,Jade Druid'),
    ('Impact',              'Demon Warlock,Highlander Priest,Jade Druid'),
    ('Seohyun628',          'Demon Warlock,Highlander Priest,Secret Mage'),
    ('BustaJ',              'Secret Mage,Tempo Rogue,Highlander Priest'),
    ('els',                 'Zoo Warlock,Tempo Rogue,Pirate Warrior'),
    ('Gaindalf',            'Big Priest,Control Paladin,Demon Warlock'),
    ('CanadianBac0nz',      'Demon Warlock,Big Priest,Jade Druid'),
    ('RLB Dexter',          'Highlander Priest,Zoo Warlock,Secret Mage'),
    ('Hayl',                'Quest Rogue,Jade Druid,Quest Mage'),
    ('mess',                'Secret Mage,Aggro Paladin,Aggro Hunter'),
    ('kd1215',              'Demon Warlock,Highlander Priest,Tempo Rogue'),
    ('Talion',              'Highlander Priest,Tempo Rogue,Aggro Paladin'),
    ('Pelletire',           'Secret Mage,Big Priest,Aggro Paladin'),
    ('trbl',                'Pirate Warrior,Zoo Warlock,Tempo Rogue'),
    ('Teebs',               'Tempo Rogue,Secret Mage,Highlander Priest'),
    ('Luker',               'Tempo Rogue,Secret Mage,Highlander Priest'),
    ('Monsanto',            'Tempo Rogue,Secret Mage,Highlander Priest'),
    ('Offbeat',             'Murloc Paladin,Highlander Priest,Secret Mage'),
    ('Bacon',               'Secret Mage,Tempo Rogue,Highlander Priest'),
    ('Fred311',             'Secret Mage,Murloc Paladin,Highlander Priest'),
    ('Level9001',           'Dragon Priest,Big Spell Mage,Token Shaman'),
    ('Yolo420blaze',        'Demon Warlock,Highlander Priest,Tempo Rogue'),
]

lineup_count = {}
decks = {}
for i,j in lineups:
    lu = tuple(sorted(j.split(',')))
    for x in lu:
        decks[x] = decks.get(x,0) + 1
    lineup_count[lu] = lineup_count.get(lu, 0) + 1
