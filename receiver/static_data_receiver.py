import socket, struct
from common.connection import Connection
from protocol.server_protocol import ServerProtocol
from common.utils import *

class StaticDataReceiver:
	def __init__(self, host, port, stations_queue, weather_queue):
		self.__connect_handlers(stations_queue, weather_queue)
		self.__connect_client(host, port)
		self.__start_receiving()

	def __connect_handlers(self, stations_queue, weather_queue):
		self.connection = Connection()
		self.stations_queue = self.connection.basic_queue(stations_queue)
		self.weather_queue = self.connection.basic_queue(weather_queue)

	def __connect_client(self, host, port):
		self.client_conn = ServerProtocol(host, port)
		self.client_conn.connect_client()

	def __start_receiving(self):
		# receive stations
		self.__receive_data(self.stations_queue)
		# receive weather
		self.__receive_data(self.weather_queue)

		self.close()

	def __receive_data(self, queue):
		eof = False
		while not eof:
			data = self.client_conn.recv()
			if not data: break
			msg = decode(data)

			if msg == "EOF":
				eof = True
				queue.send("last")
			else:
				queue.send(data)

	def close(self):
		self.client_conn.close()
		self.connection.close()