from hipchat.cards.Card import ApplicationCard, Attribute, AttributeValue, Icon
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

    storage[len(storage)] = query  # Save data to integration's volatile storage

    room = notification.item.room.id  # Retrieve numerical room ID from the request

    try:
        file_token = all_tokens["file_uploader"]  # Retrieve a global token
        upload_file(token=file_token, room=room, message="Test message", file="/tmp/test.tmp")  # Upload file to room
        send_notification(token=token, room=room, sender=__name__, message=query)  # Send notification to room
        send_message(token=token, room=room, message=query)  # Send message to the room
        send_notification(token=token,  # Send notification with card to room
                          room=notification.item.room.id,
                          message="Test message",
                          message_format='text',
                          sender="Test sender",
                          card=ApplicationCard(description="Test description\nsplit into two lines",
                                               url='https://www.application.com/an-object',
                                               title="Test title",
                                               icon=Icon(url='http://bit.ly/1S9Z5dF'),
                                               attributes=[
                                                   Attribute(label='attribute1',
                                                             value=AttributeValue(label='value2')),
                                                   Attribute(label='attribute2',
                                                             value=AttributeValue(label='value2',
                                                                                  icon=Icon(
                                                                                      url='http://bit.ly/1S9Z5dF'),
                                                                                  style='lozenge-complete'))]))
    except Exception as e:
        log.error("Whoops! Exception: " + str(e))

    log.info("Running integration done!")
