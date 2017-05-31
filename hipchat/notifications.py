import requests


def send_notification(token: str, room: str, sender: str = '', color: str = 'gray', notify: bool = False,
                      message_format: str = 'html', message: str = '', host: str = 'api.hipchat.com'):
    content = {"color": color,
               "message": message,
               "notify": notify,
               "message_format": message_format,
               "from": sender}

    url = "https://{0}/v2/room/{1}/notification".format(host, room)
    headers = {'Content-type': 'application/json',
               'Authorization': "Bearer " + token}
    response = requests.post(url, headers=headers, json=content)
    response.raise_for_status()
