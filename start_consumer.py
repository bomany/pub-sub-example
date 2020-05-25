from consumer import MessagingAPI
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('queue')
args = parser.parse_args()

queue = args.queue

print(f"Consumer Starting for queue {queue}")


def callback(ch, method, properties, body):
    print(f"Consumer with queue {queue} received a message")
    print("===========MESSAGE============")
    print(body)
    print("=============END==============")


messaging_api = MessagingAPI(
    user='rabbitmq',
    password='rabbitmq',
    url='rabbitmq',
    topic='flask_topic'
)

messaging_api.receive_message(queue=queue, callback=callback)
