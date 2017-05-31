import requests


def send_message(token: str, room: str, message: str = '', host: str = 'api.hipchat.com'):
    content = {"message": message}

    url = "https://{0}/v2/room/{1}/message".format(host, room)
    headers = {'Content-type': 'application/json',
               'Authorization': "Bearer " + token}
    response = requests.post(url, headers=headers, json=content)
    response.raise_for_status()
