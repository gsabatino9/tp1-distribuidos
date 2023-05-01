import pika, sys, os
from common.queue import BasicQueue, PubsubQueue, TopicsQueue

class Connection:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        self.channel = self.connection.channel()

    def basic_queue(self, name_queue):
        return BasicQueue(self.channel, name_queue)

    def pubsub_queue(self, name_exchange):
        return PubsubQueue(self.channel, name_exchange)

    def topic_queue(self, name_exchange, routing_key=None):
        return TopicsQueue(self.channel, name_exchange, routing_key)

    def start_receiving(self):
        self.channel.start_consuming()

    def close(self):
        self.connection.close()
        