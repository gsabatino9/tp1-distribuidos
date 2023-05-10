from server.queue.connection import Connection
from message_eof import MessageEOF
from utils import *

class EOFManager:
	def __init__(self, name_recv_queue, name_send_queue, name_stations_queue, name_weather_queue, name_join_stations_queue, name_join_weather_queue, size_workers):
		self.size_workers = size_workers
		self.acks = {i:0 for i in range(3)}
		self.__connect(name_recv_queue, name_send_queue, name_stations_queue, name_weather_queue, name_join_stations_queue, name_join_weather_queue)

	def __connect(self, name_recv_queue, name_send_queue, name_stations_queue, name_weather_queue, name_join_stations_queue, name_join_weather_queue):
		# try-except
		self.queue_connection = Connection()
		
		self.send_queue = self.queue_connection.routing_queue(name_send_queue)

		self.recv_queue = self.queue_connection.pubsub_queue(name_recv_queue)
		self.recv_queue.receive(self.receive_msg)

		self.stations_queue = self.queue_connection.basic_queue(name_stations_queue)
		self.weather_queue = self.queue_connection.basic_queue(name_weather_queue)

		self.join_stations_queue = self.queue_connection.basic_queue(name_join_stations_queue)
		self.join_weather_queue = self.queue_connection.basic_queue(name_join_weather_queue)

		self.queue_connection.start_receiving()

	def receive_msg(self, ch, method, properties, body):
		header = decode(body)

		if is_eof(header):
			self.__send_eofs(body)
		else:
			self.__recv_ack(header, body)

	def __send_eofs(self, msg):
		for i in range(self.size_workers):
			self.send_queue.send(msg, routing_key=str(i+1))

	def __recv_ack(self, header, body):
		self.acks[header.data_type] += 1

		if self.acks[header.data_type] == self.size_workers:
			if header.data_type == MessageEOF.STATION:
				self.stations_queue.send(body)
			elif header.data_type == MessageEOF.WEATHER:
				self.weather_queue.send(body)
			else:
				self.join_stations_queue.send(body)
				self.join_weather_queue.send(body)

	def stop(self):
		self.queue_connection.close()