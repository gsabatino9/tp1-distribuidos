import pika, sys, os

class Queue:
	def __init__(self, host='127.0.0.1'):
		self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
		self.channel = self.connection.channel()

	def add_queues(self, names_queues):
		for queue_name in names_queues:
			self.channel.queue_declare(queue=queue_name)

	def add_callback(self, queue_name, callback):
		self.channel.basic_consume(
			queue=queue_name,
			auto_ack=True,
			on_message_callback=callback
		)

	def start_receiving(self):
		self.channel.start_consuming()

	def send(self, queue_name, msg):
		self.channel.basic_publish(
			exchange='',
			routing_key=queue_name,
			body=msg
		)

	def close(self):
		self.connection.close()
		