from protocol.communication_server import CommunicationServer
from protocol.message_client import MessageClient
from server.queue.connection import Connection
from utils import *
import socket

class Receiver:
	def __init__(self, host, port, name_stations_queue, name_weather_queue, name_trips_queues, name_em_queue):
		# try-except a todo
		self.__connect_queue(name_stations_queue, name_weather_queue, name_trips_queues)
		self.__connect_eof_manager_queue(name_em_queue)
		client_socket = self.__connect_client(host, port)

	def __connect_queue(self, name_stations_queue, name_weather_queue, name_trips_queues):
		self.queue_connection = Connection()
		self.stations_queue = self.queue_connection.basic_queue(name_stations_queue)
		self.weather_queue = self.queue_connection.basic_queue(name_weather_queue)
		self.trips_queues = [self.queue_connection.basic_queue(q) for q in name_trips_queues]

	def __connect_eof_manager_queue(self, name_em_queue):
		self.em_queue = self.queue_connection.pubsub_queue(name_em_queue)

	def __connect_client(self, host, port):
		skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		skt.bind((host, port))
		skt.listen()

		client_socket, _ = skt.accept()
		self.client_connection = CommunicationServer(client_socket)
		return client_socket

	def run(self):
		types_ended = set()

		while len(types_ended) < 3:
			header, payload_bytes = self.client_connection.recv_data(decode_payload=False)
			
			if is_eof(header):
				types_ended.add(header.data_type)
				self.em_queue.send(eof_msg(header))
			else:
				self.__route_message(header, payload_bytes)

		print("Todos los archivos llegaron.")
		self.client_connection.send_files_received()

	def __route_message(self, header, payload_bytes):
		msg = encode_header(header) + payload_bytes
		
		if is_station(header):
			self.stations_queue.send(msg)
		elif is_weather(header):
			self.weather_queue.send(msg)
		else:
			[trips_queue.send(msg) for trips_queue in self.trips_queues]

	def stop(self):
		self.client_connection.stop()
		self.queue_connection.close()