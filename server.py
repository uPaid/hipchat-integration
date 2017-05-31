#!/usr/bin/python3
import importlib.util
import json
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from re import search

from notification import Notification

try:
    port = int(sys.argv[1])
    integrations_path = sys.argv[2]
    tokens_from_args = sys.argv[3:]
    integration_tokens = dict()
    for token in tokens_from_args:
        token_split = token.split(":")
        integration_tokens[token_split[0]] = token_split[1]
except IndexError:
    print("Usage: python3 '" + sys.argv[0] + "' [PORT] [INTEGRATIONS_PATH] [INTEGRATION_NAME:INTEGRATION_TOKEN...]")
    exit(1)


class HipChatRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        post_data = self.get_post_data()

        try:
            notification = Notification(**(json.loads(post_data)))
        except Exception as e:
            self.log_error("Exception was thrown: %s", e)
            self.send_response(400)
            return

        self.log_message("Processing message from " + notification.item.message.sender.name)
        self.log_message("Message contents: " + notification.item.message.content)

        self.send_response(204)
        self.run_integration(notification)

        return

    def get_post_data(self):
        content_length = int(self.headers['Content-Length'])
        return str(self.rfile.read(content_length), "UTF-8")

    def run_integration(self, notification: Notification):
        matcher = search(r'/(\S*) ?(.*)', notification.item.message.content)
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

        integration_module.run_integration(notification, integration_query, integration_tokens)


def run_server():
    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, HipChatRequestHandler)
    print('Running server on port', port)
    httpd.serve_forever()
