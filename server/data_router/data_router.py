from server.queue.connection import Connection
from server.eof_manager.message_eof import MessageEOF
from utils import *

class DataRouter:
	def __init__(self, id_router, name_recv_queue, name_stations_queue, name_weather_queue, name_em_queue, name_join_stations_queue, name_join_weather_queue):
		self.queue_connection = Connection()
		self.stations_queue = self.queue_connection.basic_queue(name_stations_queue)
		self.weather_queue = self.queue_connection.basic_queue(name_weather_queue)
		
		self.join_stations = self.queue_connection.basic_queue(name_join_stations_queue)
		self.join_weather = self.queue_connection.basic_queue(name_join_weather_queue)
		# falta una más -> directo a donde no quiere recibir el join

		self.recv_queue = self.queue_connection.routing_queue(name_recv_queue, routing_keys=[str(id_router)])
		self.recv_queue.receive(self.proccess_message)

		self.em_queue = self.queue_connection.pubsub_queue(name_em_queue)

		self.queue_connection.start_receiving()

	def proccess_message(self, ch, method, properties, body):
		if is_eof(body):
			self.__send_eof_ack(body)
		else:
			self.__route_message(body)

	def __send_eof_ack(self, body):
		# mando ack al eof_manager
		header = MessageEOF.decode(body)
		ack_msg = MessageEOF.ack(header.data_type)
		self.em_queue.send(ack_msg)

	def __route_message(self, body):
		header, payload_bytes = decode_header(body)
		city = obtain_city(header)

		if is_station(header):
			self.stations_queue.send(body)
		elif is_weather(header):	
			self.weather_queue.send(body)
		else:
			self.join_stations.send(body)
			self.join_weather.send(body)

	def stop(self):
		self.queue_connection.close()