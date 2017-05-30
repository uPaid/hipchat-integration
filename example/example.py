from time import sleep


def run_integration(notification, query: str):
    print("Running integration: " + __name__)
    print("Sender name: " + notification.item.message.sender.name)
    print("Message contents: " + notification.item.message.content)
    print("Query: " + query)
    sleep(5)
    print("Running integration done!")
