from hipchat.files import upload_file
from hipchat.messages import send_message
from hipchat.notifications import send_notification
from notification import Notification


def run_integration(notification: Notification, query: str, integration_token: str):
    integration_name = __name__

    print("Running integration: " + integration_name)
    print("Sender name: " + notification.item.message.sender.name)
    print("Message contents: " + notification.item.message.content)
    print("Query: " + query)

    room = notification.item.room.id

    upload_file(token="7CvE3Ur4aGD8SLMpzFxDq1Y8qzHh2wDk60FJm4H7", room=room, message="Test message",
                file="/tmp/test.tmp")
    send_notification(token=integration_token, room=room, sender=integration_name, message=query)
    send_message(token=integration_token, room=room, message=query)

    print("Running integration done!")
