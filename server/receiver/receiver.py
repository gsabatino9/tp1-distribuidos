from protocol.communication_server import CommunicationServer
from protocol.message_client import MessageClient
from server.queue.connection import Connection
from utils import *
import socket

STATION = MessageClient.STATION_DATA
WEATHER = MessageClient.WEATHER_DATA
TRIP = MessageClient.TRIP_DATA
LAST_CHUNK = MessageClient.SEND_LAST

class Receiver:
	def __init__(self, host, port, name_next_queue, name_em_queue, size_workers):
		self.actual_id = 0
		self.size_workers = size_workers

		# try-except a todo
		self.__connect_queue(name_next_queue)
		self.__connect_eof_manager_queue(name_em_queue)
		client_socket = self.__connect_client(host, port)

	def __connect_queue(self, name_next_queue):
		self.queue_connection = Connection()
		self.next_queue = self.queue_connection.routing_queue(name_next_queue)

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
		data_received = {i:0 for i in [STATION, WEATHER, TRIP]}

		while len(types_ended) < 3:
			header, payload_bytes = self.client_connection.recv_data(decode_payload=False)
			
			if header.msg_type == LAST_CHUNK:
				types_ended.add(header.data_type)
				self.em_queue.send(eof_msg(header))
			else:
				data_received[header.data_type] += 1

				msg = encode_header(header) + payload_bytes
				self.next_queue.send(msg, routing_key=self.__get_worker())

		print("Todos los archivos llegaron.")
		self.client_connection.send_files_received()

	def __get_worker(self):
		id_to_send = (self.actual_id % self.size_workers) + 1
		self.actual_id += 1

		return str(id_to_send)

	def stop(self):
		self.client_connection.stop()
		self.queue_connection.close()