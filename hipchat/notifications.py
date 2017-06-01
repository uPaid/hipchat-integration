import requests

from hipchat.cards.Card import Card


def send_notification(token: str, room: str, sender: str = '', color: str = 'gray', notify: bool = False,
                      message_format: str = 'html', message: str = '', host: str = 'api.hipchat.com',
                      card: Card = None):
    available_formats = ['html', 'text']
    if message_format not in available_formats:
        raise ValueError("Format '" + message_format + "' is invalid. Available formats: " + str(available_formats))

    content = {"color": color,
               "message": message,
               "notify": notify,
               "message_format": message_format,
               "from": sender}

    if card is not None:
        content['card'] = card.__dict__

    url = "https://{0}/v2/room/{1}/notification".format(host, room)
    headers = {'Content-type': 'application/json',
               'Authorization': "Bearer " + token}
    response = requests.post(url, headers=headers, json=content)
    response.raise_for_status()
