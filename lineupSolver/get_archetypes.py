import json
#import requests

#url = 'https://hsreplay.net/api/v1/archetypes/?format=json'
#payload = json.load(open("request.json"))
#headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
#r = requests.post(url, data=json.dumps(payload), headers=headers)
#r = requests.post(url, headers=headers)

#r = requests.get('https://hsreplay.net/api/v1/archetypes/')
#r = requests.get('https://hsreplay.net/api/v1/archetypes/?format=json')
#archetypes_json = json.loads(r.content)
#NOTE FIGURE OUT A WAY TO KEEP CLEAN

importNew = False
if importNew:
    import os
    os.system('curl https://hsreplay.net/api/v1/archetypes/?format=json > archetypes.json')

from config import *
archetypes_json = json.load(open(basedir + '/lineupSolver/archetypes.json'))

archetype_names = {}
archetype_ids = {}
for archetype in archetypes_json:
    archetype_names[archetype['id']] = archetype['name']
    archetype_ids[archetype['name']] = archetype['id']

def get_archetype(arch_id):
    res = archetype_names.get(int(arch_id))
    return res
