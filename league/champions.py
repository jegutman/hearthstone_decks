import json

champs_by_id = {}
champ_data = json.load(open('champion.json'))['data']
for i in champ_data.keys():
    champs_by_id[int(champ_data[i]['key'])] = i
