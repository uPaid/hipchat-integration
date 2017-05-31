import json
import os

import requests


def upload_file(token: str, room: str, file: str, message='', host: str = 'api.hipchat.com'):
    if not os.path.isfile(file):
        raise ValueError("File '{0}' does not exist".format(file))
    if len(message) > 1000:
        raise ValueError('Message too long')

    url = "https://{0}/v2/room/{1}/share/file".format(host, room)
    headers = {'Content-type': 'multipart/related; boundary=boundary123456',
               'Authorization': "Bearer " + token}
    msg = json.dumps({'message': message})

    payload = """\
--boundary123456
Content-Type: application/json; charset=UTF-8
Content-Disposition: attachment; name="metadata"
{0}
--boundary123456
Content-Disposition: attachment; name="file"; filename="{1}"
{2}
--boundary123456--\
""".format(msg, os.path.basename(file), open(file, 'rb').read())

    response = requests.post(url, headers=headers, data=payload)
    response.raise_for_status()
