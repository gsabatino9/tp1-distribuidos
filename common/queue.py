import pika

class Queue:
	def __init__(self, channel, queue_name='', exchange_name=None, exchange_type=None, routing_key=None):
		self.queue_name = queue_name
		self.exchange_name = exchange_name
		self.exchange_type = exchange_type
		self.routing_key = routing_key
		self.channel = channel

		self.__start_queue()

	def __start_queue(self):
		if self.exchange_name:
			self.channel.exchange_declare(exchange=self.exchange_name, exchange_type=self.exchange_type)
		else:
			self.channel.basic_qos(prefetch_count=1)
			self.channel.queue_declare(queue=self.queue_name)

	def send(self, message):
		exchange = self.exchange_name if self.exchange_name else ''
		routing = self.routing_key if self.routing_key else self.queue_name

		self.channel.basic_publish(
			exchange=exchange, 
			routing_key=routing, 
			body=message
		)

	def receive(self, callback):
		self.__bind_queue()

		self.channel.basic_consume(
			queue=self.queue_name, 
			on_message_callback=callback, 
			auto_ack=True
		)

	def __bind_queue(self):
		if self.exchange_name:
			result = self.channel.queue_declare(queue='', exclusive=True)
			self.queue_name = result.method.queue
			self.channel.queue_bind(exchange=self.exchange_name, queue=self.queue_name)

			if self.routing_key:
				self.channel.queue_bind(queue=self.queue_name, exchange=self.exchange_name, routing_key=self.routing_key)

class BasicQueue(Queue):
	def __init__(self, channel, name_queue):
		super().__init__(channel, queue_name=name_queue)

class PubsubQueue(Queue):
	def __init__(self, channel, exchange_name):
		super().__init__(channel, exchange_name=exchange_name, exchange_type='fanout')

class TopicsQueue(Queue):
	def __init__(self, channel, exchange_name, routing_key=None):
		super().__init__(channel, exchange_name=exchange_name, exchange_type='topic', routing_key=routing_key)

"""
class WorkersQueue(Queue):
	def __init__(self, exchange_name, exchange_type='direct', routing_key=None, is_sender=False, is_receiver=False):
		super().__init__('workers_queue', exchange_name=exchange_name, exchange_type=exchange_type, routing_key=routing_key, is_sender=is_sender, is_receiver=is_receiver)

class RoutingQueue(Queue):
	def __init__(self, exchange_name, exchange_type='direct', routing_key=None, is_sender=False, is_receiver=False):
		super().__init__('routing_queue', exchange_name=exchange_name, exchange_type=exchange_type, routing_key=routing_key, is_sender=is_sender, is_receiver=is_receiver)


"""