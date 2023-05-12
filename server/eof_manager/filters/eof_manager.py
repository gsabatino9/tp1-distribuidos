from server.queue.connection import Connection
from server.eof_manager.common.message_eof import MessageEOF
from server.eof_manager.common.utils import *

class EOFManager:
	def __init__(self, name_recv_queue, name_filters_queue, size_workers):
		self.size_workers = size_workers
		self.acks = 0
		self.__connect(name_recv_queue, name_filters_queue)

	def __connect(self, name_recv_queue, name_filters_queue):
		# try-except
		self.queue_connection = Connection()
		
		self.recv_queue = self.queue_connection.pubsub_queue(name_recv_queue)
		self.recv_queue.receive(self.receive_msg)

		self.filters_queue = self.queue_connection.basic_queue(name_filters_queue)

		self.queue_connection.start_receiving()

	def receive_msg(self, ch, method, properties, body):
		header = decode(body)

		if is_eof(header):
			print("EOF recv")
			self.__send_eofs(header, body)
		else:
			self.__recv_ack_trips(header, body)

	def __send_eofs(self, header, msg):
		for _ in range(self.size_workers):
			self.filters_queue.send(msg)

	def __recv_ack_trips(self, header, body):
		self.acks += 1

		if self.acks == self.size_workers:
			print("EOF trips ackeados.")

	def stop(self):
		self.queue_connection.close()