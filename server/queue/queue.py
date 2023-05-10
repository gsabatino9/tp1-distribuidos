import pika

class Queue:
	def __init__(self, channel, queue_name='', exchange_name=None, exchange_type=None, routing_keys=None):
		self.queue_name = queue_name
		self.exchange_name = exchange_name
		self.exchange_type = exchange_type
		self.routing_keys = routing_keys
		self.channel = channel

		self.__start_queue()

	def __start_queue(self):
		if self.exchange_name:
			self.channel.exchange_declare(exchange=self.exchange_name, exchange_type=self.exchange_type)
		else:
			self.channel.basic_qos(prefetch_count=1)
			self.channel.queue_declare(queue=self.queue_name)

	def send(self, message, routing_key=None):
		exchange = self.exchange_name if self.exchange_name else ''
		routing = routing_key if routing_key else self.queue_name

		self.channel.basic_publish(
			exchange=exchange, 
			routing_key=routing, 
			body=message
		)

	def receive(self, callback, auto_ack=True):
		self.__bind_queue()

		self.channel.basic_consume(
			queue=self.queue_name, 
			on_message_callback=callback, 
			auto_ack=auto_ack
		)

	def __bind_queue(self):
		if self.exchange_name:
			result = self.channel.queue_declare(queue='', exclusive=True)
			self.queue_name = result.method.queue
			if self.routing_keys:
				for routing_key in self.routing_keys:
					self.channel.queue_bind(queue=self.queue_name, exchange=self.exchange_name, routing_key=routing_key)
			else:
				self.channel.queue_bind(exchange=self.exchange_name, queue=self.queue_name)

class BasicQueue(Queue):
	def __init__(self, channel, name_queue):
		super().__init__(channel, queue_name=name_queue)

class PubsubQueue(Queue):
	def __init__(self, channel, exchange_name):
		super().__init__(channel, exchange_name=exchange_name, exchange_type='fanout')

class RoutingQueue:
	def __init__(self, channel, exchange_name, routing_keys, auto_ack=True):
		self.channel = channel
		self.exchange_name = exchange_name
		self.auto_ack = auto_ack
		self.__build_queue(routing_keys)

	def __build_queue(self, routing_keys):
		self.channel.exchange_declare(exchange=self.exchange_name,
						 exchange_type='direct')

		result = self.channel.queue_declare(queue='', exclusive=True)
		self.queue_name = result.method.queue

		for routing_key in routing_keys:
			self.channel.queue_bind(exchange=self.exchange_name,
							   queue=self.queue_name,
							   routing_key=routing_key)

	def receive(self, callback):
		self.channel.basic_consume(
			queue=self.queue_name, on_message_callback=callback, auto_ack=self.auto_ack)

	def send(self, message, routing_key):
		self.channel.basic_publish(exchange=self.exchange_name,
					  routing_key=routing_key,
					  body=message)