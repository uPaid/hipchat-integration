from hipchat.files import upload_file
from hipchat.messages import send_message
from hipchat.notifications import send_notification
from notification import Notification


def run_integration(notification: Notification, query: str, integration_tokens: dict):
    integration_name = __name__

    print("Running integration: " + integration_name)

    integration_token = integration_tokens["example"]
    print("Token: " + integration_token)
    print("Sender name: " + notification.item.message.sender.name)
    print("Message contents: " + notification.item.message.content)
    print("Query: " + query)

    room = notification.item.room.id

    upload_file(token=integration_token, room=room, message="Test message",
                file="/tmp/test.tmp")
    send_notification(token=integration_token, room=room, sender=integration_name, message=query)
    send_message(token=integration_token, room=room, message=query)

    print("Running integration done!")
