from server.queue.connection import Connection
from server.eof_manager.common.message_eof import MessageEOF
from server.eof_manager.common.utils import *

class EOFManager:
	def __init__(self, name_recv_queue, name_groupby_queues):
		self.acks = 0
		self.__connect(name_recv_queue, name_groupby_queues)

	def __connect(self, name_recv_queue, name_groupby_queues):
		# try-except
		self.queue_connection = Connection()
		
		self.recv_queue = self.queue_connection.pubsub_queue(name_recv_queue)
		self.recv_queue.receive(self.receive_msg)

		self.groupby_queues = [self.queue_connection.basic_queue(q) for q in name_groupby_queues]

		self.queue_connection.start_receiving()

	def receive_msg(self, ch, method, properties, body):
		header = decode(body)

		if is_eof(header):
			self.__send_eofs(header, body)
		else:
			self.__recv_ack_trips(header, body)

	def __send_eofs(self, header, msg):
		for q in self.groupby_queues:
			q.send(msg)

	def __recv_ack_trips(self, header, body):
		self.acks += 1

		if self.acks == len(self.groupby_queues):
			print("EOF trips ackeados.")

	def stop(self):
		self.queue_connection.close()