import threading
from functools import partial
import pika


class AMQPConsuming(threading.Thread):
    def __init__(self, callback, *args, **kwargs):
        self.callback = callback
        super(AMQPConsuming, self).__init__(*args, **kwargs)

    def run(self):
        self.callback()


class MessagingAPI:

    def __init__(self, user, password, url, topic):
        self.credentials = pika.PlainCredentials(user, password)
        self.connection_params = pika.ConnectionParameters(url, credentials=self.credentials)
        self.topic = topic

    def send_message(self, message):
        with pika.BlockingConnection(self.connection_params) as connection:
            channel = connection.channel()

            channel.exchange_declare(exchange=self.topic, exchange_type='fanout')

            channel.basic_publish(
                exchange=self.topic,
                routing_key='',
                body=message
            )

    def receive_message(self, queue, callback):
        with pika.BlockingConnection(self.connection_params) as connection:
            channel = connection.channel()

            channel.exchange_declare(exchange=self.topic, exchange_type='fanout')
            channel.queue_declare(queue=queue)
            channel.queue_bind(exchange=self.topic, queue=queue)

            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(on_message_callback=callback, queue=queue, auto_ack=True)
            channel.start_consuming()

    def start_consumer(self, queue, callback):
        consumer = AMQPConsuming(callback=partial(self.receive_message, queue, callback))
        consumer.daemon = True
        consumer.start()
