import socket, struct
from common.connection import Connection
from protocol.server_protocol import ServerProtocol

class TripsReceiver:
	def __init__(self, host, port, trips_queues, em_queue):
		self.__connect_queues(trips_queues, em_queue)
		self.__connect_client(host, port)
		self.__start_receiving()

	def __connect_queues(self, trips_queues, em_queue):
		self.connection = Connection()
		self.send_queues = [self.connection.basic_queue(q) for q in trips_queues]
		self.em_queue = self.connection.pubsub_queue(em_queue)

	def __connect_client(self, host, port):
		self.client_conn = ServerProtocol(host, port)
		self.client_conn.connect_client()

	def __start_receiving(self):
		self.eof = False
		while not self.eof:
			data = self.client_conn.recv()
			if not data: break
			msg = data.decode('utf-8')

			if msg == "EOF":
				self.eof = True
				self.em_queue.send(msg)
			else:
				for queue in self.send_queues:
					queue.send(data)
		
		self.close()

	def close(self):
		self.client_conn.close()
		self.connection.close()