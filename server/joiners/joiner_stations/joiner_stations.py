from server.queue.connection import Connection
from utils import *

class JoinerStations:
	"""
	Guarda toda la información de Stations, para
	una ciudad dada.
	"""

	def __init__(self, name_recv_queue, name_trips_queue):
		self.joiner = StationsData()
		self.__connect(name_recv_queue, name_trips_queue)
		
	def __connect(self, name_recv_queue, name_trips_queue):
		self.queue_connection = Connection()
		self.recv_queue = self.queue_connection.basic_queue(name_recv_queue)
		self.trips_queue = self.queue_connection.basic_queue(name_trips_queue)

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

		for trip in trips:
			trip = trip.split(',')
			ret = self.joiner.join_trip(city, trip)
			if ret: self.amount_joined += 1
			#else: print(f"Error: {trip}")

	def __last_trip_arrived(self):
		print(f"EOF trips - enviando eof a siguiente etapa. Joined: {self.amount_joined}")


	def stop(self):
		self.queue_connection.close()