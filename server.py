#!/usr/bin/python3
import importlib.util
import json
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from json.decoder import JSONDecodeError
from re import search

from notification import Notification
from threads import async

port = int(sys.argv[1])
integrations_path = sys.argv[2]


class HipChatRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        post_data = self.get_post_data()

        try:
            notification = Notification(**(json.loads(post_data)))
        except JSONDecodeError as e:
            self.log_error("Exception was thrown: %s", e)
            self.send_response(400)
            return

        self.log_message("Processing message from " + notification.item.message.sender.name)
        self.log_message("Message contents: " + notification.item.message.content)

        self.run_integration(notification)

        self.send_response(204)
        return

    def get_post_data(self):
        content_length = int(self.headers['Content-Length'])
        return str(self.rfile.read(content_length), "UTF-8")

    @async
    def run_integration(self, notification: Notification):
        matcher = search(r'/(\S*) (.*)', notification.item.message.content)
        integration_name = matcher.group(1)
        integration_query = matcher.group(2)
        integration_path = integrations_path + "/" + integration_name + ".py"

        spec = importlib.util.spec_from_file_location(integration_name, integration_path)
        integration_module = importlib.util.module_from_spec(spec)

        try:
            spec.loader.exec_module(integration_module)
        except FileNotFoundError:
            self.log_error("Integration '" + integration_name + "' could not be found")
            return

        integration_module.run_integration(notification, integration_query)


def run_server():
    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, HipChatRequestHandler)
    print('Running server on port', port)
    httpd.serve_forever()
