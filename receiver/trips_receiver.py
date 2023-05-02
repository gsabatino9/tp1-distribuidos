import socket, struct
from common.connection import Connection

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
		self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self._server_socket.bind((host, port))
		self._server_socket.listen()
		
		client_socket, addr = self._server_socket.accept()
		self.client_socket = client_socket

	def __start_receiving(self):
		self.eof = False
		while not self.eof:
			data = self.client_socket.recv(4)
			if not data: break
			len_msg = struct.unpack('!i', data)[0]

			data = self.client_socket.recv(len_msg)
			if not data: break
			msg = data.decode('utf-8')

			if msg == "EOF":
				self.eof = True
				self.em_queue.send(msg)
			else:
				for queue in self.send_queues:
					queue.send(bytes(msg, 'utf-8'))
		
		self.close()

	def close(self):
		self.client_socket.close()
		self._server_socket.close()
		self.connection.close()

HOST = 'server'
PORT = 12346
TRIPS_QUEUE = "trips_queue"
JOIN_TRIPS_STATIONS_QUEUE = "join_trip_station_queue"
EM_QUEUE = "eof_handler_queue"

if __name__ == "__main__":
	TripsReceiver(HOST, PORT, [TRIPS_QUEUE, JOIN_TRIPS_STATIONS_QUEUE], EM_QUEUE)