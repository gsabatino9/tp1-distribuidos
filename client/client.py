import socket, struct, time, os
import data.Montreal, data.Washington, data.Toronto
from protocol.client_protocol import ClientConnection

class Client:
	def __init__(self, host, port_static, port_trips):
		self.host = host
		self.port_static = port_static
		self.port_trips = port_trips

	def run(self):
		self.__send_static_data()
		time.sleep(3)
		self.__send_trips()

	def __send_static_data(self):
		self.static_conn = ClientConnection(self.host, self.port_static)
		self.__send_stations()
		self.__send_weather()
		self.static_conn.close()

	def __send_stations(self):
		cities = [data.Montreal.stations, data.Toronto.stations, data.Washington.stations]

		for i, city in enumerate(["Montreal", "Toronto", "Washington"]):
			stations = cities[i]
			for msg in stations:
				self.static_conn.send(city, msg)

		self.static_conn.eof()

	def __send_weather(self):
		cities = [data.Montreal.weathers, data.Toronto.weathers, data.Washington.weathers]
		
		for i, city in enumerate(["Montreal", "Toronto", "Washington"]):
			weather = cities[i]
			for msg in weather:
				self.static_conn.send(city, msg)

		self.static_conn.eof()

	def __send_trips(self):
		self.trips_conn = ClientConnection(self.host, self.port_trips)
		cities = [data.Montreal.trips, data.Toronto.trips, data.Washington.trips]

		for i, city in enumerate(["Montreal", "Toronto", "Washington"]):
			trips = cities[i]
			for msg in trips:
				self.trips_conn.send(city, msg)
		
		self.trips_conn.eof()
		self.trips_conn.close()
