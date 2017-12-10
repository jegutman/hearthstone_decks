import json
import requests

#url = 'https://hsreplay.net/api/v1/archetypes/?format=json'
#payload = json.load(open("request.json"))
#headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
#r = requests.post(url, data=json.dumps(payload), headers=headers)
#r = requests.post(url, headers=headers)

#r = requests.get('https://hsreplay.net/api/v1/archetypes/')
#r = requests.get('https://hsreplay.net/api/v1/archetypes/?format=json')
#archetypes_json = json.loads(r.content)
import os
os.system('curl https://hsreplay.net/api/v1/archetypes/?format=json > archetypes.json')

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
    if res:
        if res[-4:] == 'lock' and res.split(' ')[-1] != 'Warlock':
            res += ' Warlock'
    #return resMap.get(res, res)
    return res

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


