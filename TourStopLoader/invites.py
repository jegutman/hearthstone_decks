import json
import requests

data = json.loads(requests.get('https://majestic.battlefy.com/hearthstone-masters/invitees?tourStop=Las+Vegas').text)
for i in data:
    print(",".join(i.values()))
