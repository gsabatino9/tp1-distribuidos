import pika, sys, os
from server.queue.queue import BasicQueue, PubsubQueue, RoutingQueue

class Connection:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        self.channel = self.connection.channel()

    def basic_queue(self, name_queue):
        return BasicQueue(self.channel, name_queue)

    def pubsub_queue(self, name_exchange):
        return PubsubQueue(self.channel, name_exchange)

    def routing_queue(self, exchange_name, routing_keys=[]):
        return RoutingQueue(self.channel, exchange_name, routing_keys)

    def start_receiving(self):
        self.channel.start_consuming()

    def stop_receiving(self):
        self.channel.stop_consuming()

    def close(self):
        self.connection.close()
        