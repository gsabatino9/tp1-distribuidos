import socket, struct
from common.connection import Connection
from protocol.server_protocol import ServerProtocol
from common.utils import *

class StaticDataReceiver:
	def __init__(self, host, port, stations_queue):
		self.__connect_handlers(stations_queue)
		self.__connect_client(host, port)
		self.__start_receiving()

	def __connect_handlers(self, stations_queue):
		self.connection = Connection()
		self.stations_queue = self.connection.basic_queue(stations_queue)

	def __connect_client(self, host, port):
		self.client_conn = ServerProtocol(host, port)
		self.client_conn.connect_client()

	def __start_receiving(self):
		self.eof = False
		while not self.eof:
			data = self.client_conn.recv()
			if not data: break
			msg = decode(data)

			if msg == "EOF":
				self.eof = True
				self.stations_queue.send("last")
			else:
				self.stations_queue.send(data)

		self.close()

	def close(self):
		self.client_conn.close()
		self.connection.close()

HOST = 'server'
PORT = 12345
STATIONS_QUEUE = "stations_queue"

if __name__ == "__main__":
	StaticDataReceiver(HOST, PORT, STATIONS_QUEUE)