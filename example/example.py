from hipchat.files import upload_file
from hipchat.messages import send_message
from hipchat.notifications import send_notification
from notification import Notification
from server import Logger


def run_integration(notification: Notification, query: str, all_tokens: dict, token: str, storage: dict, log: Logger):
    log.info("Running integration: %s" % __name__)
    log.info("Sender name: %s" % notification.item.message.sender.name)
    log.info("Message contents: %s" % notification.item.message.content)
    log.info("Query: %s" % query)

    storage[len(storage)] = query  # Saves data to integration's volatile storage

    room = notification.item.room.id  # Retrieves numerical room ID from the request

    try:
        file_token = all_tokens["file_uploader"]  # Retrieves a global token
        upload_file(token=file_token, room=room, message="Test message", file="/tmp/test.tmp")  # Uploads file to room
        send_notification(token=token, room=room, sender=__name__, message=query)  # Sends notification to room
        send_message(token=token, room=room, message=query)  # Sends message to room
    except Exception as e:
        log.error("Whoops! Exception: " + str(e))

    log.info("Running integration done!")
