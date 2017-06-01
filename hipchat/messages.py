import json

import requests

from hipchat.cards.Card import Card


def send_message(token: str, room: str, message: str = '', host: str = 'api.hipchat.com', card: Card = None):
    content = {"message": message}
    if card is not None:
        content['card'] = card.__dict__

    print(json.dumps(content, indent=4))

    url = "https://{0}/v2/room/{1}/message".format(host, room)
    headers = {'Content-type': 'application/json',
               'Authorization': "Bearer " + token}
    response = requests.post(url, headers=headers, json=content)
    response.raise_for_status()
