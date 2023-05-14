import signal, sys
from server.common.queue.connection import Connection
from server.common.utils_messages_eof import *

class EOFManager:
	def __init__(self, name_recv_queue, name_verifier_queue, size_queries):
		self.__init_eof_manager(size_queries)

		self.__connect(name_recv_queue, name_verifier_queue)
		self.recv_queue.receive(self.receive_msg)
		self.queue_connection.start_receiving()

	def __init_eof_manager(self, size_queries):
		self.running = True
		signal.signal(signal.SIGTERM, self.stop)

		self.acks = 0
		self.size_queries = size_queries

	def __connect(self, name_recv_queue, name_verifier_queue):
		# try-except
		self.queue_connection = Connection()
		self.recv_queue = self.queue_connection.pubsub_queue(name_recv_queue)
		self.verifier_queue = self.queue_connection.routing_queue(name_verifier_queue)		

	def receive_msg(self, ch, method, properties, body):
		header = decode(body)

		if is_eof(header):
			self.__send_eofs(header, body)
		else:
			self.__recv_ack_trips(header, body)

	def __send_eofs(self, header, msg):
		for i in range(1, self.size_queries+1):
			self.verifier_queue.send(msg, routing_key=str(i))

	def __recv_ack_trips(self, header, body):
		self.acks += 1

		if self.acks == self.size_queries:
			print("EOF trips ackeados.")

	def stop(self, *args):
		if self.running:
			self.queue_connection.stop_receiving()
			self.queue_connection.close()
			
			self.running = False
			print("EOFManagerResultsVerifier cerrado correctamente.")

		sys.exit(0)