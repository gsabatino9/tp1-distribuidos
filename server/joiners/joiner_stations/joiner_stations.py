from server.common.queue.connection import Connection
from utils import StationsData
from server.common.utils_messages_client import *
from server.common.utils_messages_eof import ack_msg

class JoinerStations:
	def __init__(self, name_recv_queue, name_trips_queue, name_em_queue, name_next_stage_queue):
		self.joiner = StationsData()
		self.__connect(name_recv_queue, name_trips_queue, name_em_queue, name_next_stage_queue)
		
	def __connect(self, name_recv_queue, name_trips_queue, name_em_queue, name_next_stage_queue):
		self.queue_connection = Connection()
		self.recv_queue = self.queue_connection.basic_queue(name_recv_queue)
		self.trips_queue = self.queue_connection.basic_queue(name_trips_queue)
		self.em_queue = self.queue_connection.pubsub_queue(name_em_queue)
		self.next_stage_queue = self.queue_connection.pubsub_queue(name_next_stage_queue)

		self.recv_queue.receive(self.process_stations_messages)
		self.queue_connection.start_receiving()

	def process_stations_messages(self, ch, method, properties, body):
		if is_eof(body):
			self.__last_station_arrived()
		else:
			self.__station_arrived(body)

	def __last_station_arrived(self):
		print(f"Todas las stations llegaron")
		self.amount_joined = 0
		self.trips_queue.receive(self.process_join_messages)

	def __station_arrived(self, body):
		header, stations = decode(body)
		city = obtain_city(header)

		for station in stations:
			station = station.split(',')
			self.joiner.add_station(city, station)

	def process_join_messages(self, ch, method, properties, body):
		if is_eof(body):
			self.__last_trip_arrived()
		else:
			self.__request_join_arrived(body)

	def __request_join_arrived(self, body):
		header, trips = decode(body)
		city = obtain_city(header)
		joined_trips = []

		for trip in trips:
			trip = trip.split(',')
			ret = self.joiner.join_trip(city, trip)
			if ret: 
				self.amount_joined += 1
				joined_trips.append(ret)

		self.__send_next_stage(header, joined_trips)

	def __send_next_stage(self, header, joined_trips):
		if len(joined_trips) > 0:
			msg = construct_msg(header, joined_trips)
			self.next_stage_queue.send(msg)

	def __last_trip_arrived(self):
		self.em_queue.send(ack_msg())
		print(f"EOF trips - Joined: {self.amount_joined}")

	def stop(self):
		self.queue_connection.close()