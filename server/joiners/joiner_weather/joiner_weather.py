from server.queue.connection import Connection
from utils import *

class JoinerWeather:
	"""
	Guarda toda la información de Weather, para
	una ciudad dada.
	"""

	def __init__(self, name_recv_queue, name_trips_queue):
		self.joiner = WeatherData()
		self.__connect(name_recv_queue, name_trips_queue)
		
	def __connect(self, name_recv_queue, name_trips_queue):
		self.queue_connection = Connection()
		self.recv_queue = self.queue_connection.basic_queue(name_recv_queue)
		self.trips_queue = self.queue_connection.basic_queue(name_trips_queue)

		self.recv_queue.receive(self.process_weathers_messages)
		self.queue_connection.start_receiving()

	def process_weathers_messages(self, ch, method, properties, body):
		if is_eof(body):
			self.__last_weather_arrived()
		else:
			self.__weather_arrived(body)

	def __last_weather_arrived(self):
		print(f"Todas los weather llegaron")
		self.amount_joined = 0
		self.trips_queue.receive(self.process_join_messages)

	def __weather_arrived(self, body):
		header, weathers = decode(body)
		city = obtain_city(header)

		for weather in weathers:
			weather = weather.split(',')
			self.joiner.add_weather(city, weather)

	def process_join_messages(self, ch, method, properties, body):
		if is_eof(body):
			self.__last_trip_arrived()
		else:
			self.__request_join_arrived(body)

	def __request_join_arrived(self, body):
		header, trips = decode(body)
		city = obtain_city(header)
		filtered = 0

		for trip in trips:
			trip = trip.split(',')
			ret = self.joiner.join_trip(city, trip)
			if ret: 
				self.amount_joined += 1
			else:
				filtered += 1

		if filtered > 0: print("Filtered: ", filtered)

	def __last_trip_arrived(self):
		print(f"EOF trips - enviando eof a siguiente etapa. Joined: {self.amount_joined}")

	def stop(self):
		self.queue_connection.close()