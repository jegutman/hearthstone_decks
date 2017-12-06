import json
#import requests

#r = requests.get('https://hsreplay.net/api/v1/archetypes/')
#archetypes_json = json.loads(r.content)

archetypes_json = json.load(open('archetypes.json'))

archetype_names = {}
archetype_ids = {}
for archetype in archetypes_json:
    archetype_names[archetype['id']] = archetype['name']
    archetype_ids[archetype['name']] = archetype['id']


resMap = {
    'Zoolock': 'Zoo Warlock',
}

def get_archetype(arch_id):
    res = archetype_names.get(int(arch_id))
    return resMap.get(res, res)

vs_arch_map = {
    'Tempo Rogue'       : 'Tempo Rogue',
    'Razakus Priest'    : 'Highlander Priest',
    'Zoo Warlock'       : 'Zoolock',
    'Aggro-Token Druid' : 'Aggro Druid',
    'Jade Druid'        : 'Jade Druid',
    'Big Druid'         : 'Big Druid',
    'Big Priest'        : 'Big Priest',
    'Control Mage'      : 'Control Mage',
    'Midrange Hunter'   : 'Midrange Hunter',
    'Token Shaman'      : 'Token Shaman',
    'Control Warlock'   : 'Control Warlock',
    'Murloc Paladin'    : 'Murloc Paladin',
    'Secret Mage'       : 'Secret Mage',
    'Exodia Mage'       : 'Exodia Mage',
    'Dragon Priest'     : 'Dragon Priest',
    'Miracle Rogue'     : 'Miracle Rogue',
}


