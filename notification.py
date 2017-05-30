#!/usr/bin/python3


class Sender:
    def __init__(self, id: int, links: dict, mention_name: str, name: str, version: str):
        self.id = id
        self.links = links
        self.mention_name = mention_name
        self.name = name
        self.version = version


class Room:
    def __init__(self, id: int, is_archived: bool, links: dict, name: str, privacy: str, version: str):
        self.id = id
        self.is_archived = is_archived
        self.links = links
        self.name = name
        self.privacy = privacy
        self.version = version


class Message:
    def __init__(self, date: str, id: str, message: str, type: str, **kwargs):
        self.date = date
        self.id = id
        self.content = message
        self.type = type
        self.sender = Sender(**kwargs['from'])


class Item:
    def __init__(self, message: dict, room: dict):
        self.message = Message(**message)
        self.room = Room(**room)


class Notification:
    def __init__(self, event: str, item: dict, oauth_client_id: str, webhook_id: int):
        self.event = event
        self.item = Item(**item)
        self.oauth_client_id = oauth_client_id
        self.web_hook = webhook_id
