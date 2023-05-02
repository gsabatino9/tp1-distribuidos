import socket, struct
from common.connection import Connection

class StaticDataReceiver:
	def __init__(self, host, port, stations_queue):
		self.__connect_handlers(stations_queue)
		self.__connect_client(host, port)
		self.__start_receiving()

	def __connect_handlers(self, stations_queue):
		self.connection = Connection()
		self.stations_queue = self.connection.basic_queue(stations_queue)

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

			print(f"len: {len_msg} - msg: {msg}")

			if msg == "EOF":
				self.eof = True
				self.stations_queue.send("last")
			else:
				self.stations_queue.send(msg)

		self.close()

	def close(self):
		self.client_socket.close()
		self._server_socket.close()
		self.connection.close()

HOST = 'server'
PORT = 12345
STATIONS_QUEUE = "stations_queue"

if __name__ == "__main__":
	StaticDataReceiver(HOST, PORT, STATIONS_QUEUE)