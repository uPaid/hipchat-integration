#!/usr/bin/python3
import importlib.util
import json
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from re import search

from notification import Notification
from threads import async

try:
    port = int(sys.argv[1])
    integrations_path = sys.argv[2]
    tokens_from_args = sys.argv[3:]
    integration_tokens = dict()
    for token in tokens_from_args:
        token_split = token.split(":")

        token_id = token_split[0]
        if len(token_split) == 2:  # Global token in format name:value
            if token_id in integration_tokens:
                raise ValueError("Duplicate token name: " + token_id)
            integration_tokens[token_id] = token_split[1]

        elif len(token_split) == 3:  # Room-specific token in format room:name:value
            if token_id not in integration_tokens:
                integration_tokens[token_id] = dict()
            if token_split[1] in integration_tokens[token_id]:
                raise ValueError("Duplicate token name: " + token_id + " for room " + token_id)
            integration_tokens[token_id][token_split[1]] = token_split[2]

except IndexError:
    print("Usage: python3 '" + sys.argv[0] + "' [PORT] [INTEGRATIONS_PATH] [INTEGRATION_NAME:INTEGRATION_TOKEN...]")
    exit(1)


class Logger:
    def __init__(self, request_handler, integration_name: str, ref: str):
        self.__request_handler = request_handler
        self.__integration_name = integration_name
        self.__ref = ref

    def info(self, message):
        self.__request_handler.log_message(format="(" + self.__ref + ") " + self.__integration_name + " : " + message)

    def error(self, message):
        self.__request_handler.log_error(format="(" + self.__ref + ") " + self.__integration_name + " : " + message)


class HipChatRequestHandler(BaseHTTPRequestHandler):
    __STORAGE = dict()

    def log_message(self, format, *args):  # We want to log messages to stdout instead of stderr
        sys.stdout.write("%s - - [%s] %s\n" %
                         (self.address_string(),
                          self.log_date_time_string(),
                          format % args))

    def do_POST(self):
        post_data = self.get_post_data()

        if post_data[0:4] == "save":  # Save storage to file
            file_name = post_data[5:]
            self.log_message("Writing storage to file " + file_name)
            with open(file_name, 'w') as file:
                file.write(json.dumps(HipChatRequestHandler.__STORAGE, indent=4))
            return

        if post_data[0:4] == "load":  # Read storage from file
            file_name = post_data[5:]
            self.log_message("Loading storage from file " + file_name)
            with open(file_name, 'r') as file:
                HipChatRequestHandler.__STORAGE = json.loads(" ".join(file.readlines()))
            return

        if post_data[0:5] == "erase":  # Erase storage
            self.log_message("Erasing storage")
            HipChatRequestHandler.__STORAGE = dict()

        try:  # Parse request from HipChat
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

    @async  # We want to run it in a new thread
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

        if integration_name not in HipChatRequestHandler.__STORAGE:
            HipChatRequestHandler.__STORAGE[integration_name] = dict()

        current_token = None
        room_id = str(notification.item.room.id)
        if room_id in integration_tokens:
            if integration_name in integration_tokens[room_id]:
                current_token = integration_tokens[room_id][integration_name]

        ref = str(integration_module.run_integration)[31: 43]  # Pseudo trace ID
        integration_module.run_integration(notification=notification,
                                           query=integration_query,
                                           all_tokens=integration_tokens,
                                           token=current_token,
                                           storage=HipChatRequestHandler.__STORAGE[integration_name],
                                           log=Logger(self, integration_name, ref))


def run_server():
    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, HipChatRequestHandler)
    print('Running server on port', port)
    httpd.serve_forever()
