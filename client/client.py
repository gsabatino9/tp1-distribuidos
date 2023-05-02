import socket, struct, time, os, csv
from protocol.client_protocol import ClientConnection

class Client:
	def __init__(self, host, port_static, port_trips):
		self.host = host
		self.port_static = port_static
		self.port_trips = port_trips
		self.cities = ["Montreal", "Toronto", "Washington"]

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
		for i, city in enumerate(self.cities):
			with open(f'/data/{city}/stations.csv', newline='') as csvfile:
				reader = csv.reader(csvfile, delimiter=',')
				for msg in reader:
					self.static_conn.send(city, ','.join(msg))

		self.static_conn.eof()

	def __send_weather(self):		
		for i, city in enumerate(self.cities):
			with open(f'/data/{city}/weather.csv', newline='') as csvfile:
				reader = csv.reader(csvfile, delimiter=',')
				for msg in reader:
					self.static_conn.send(city, ','.join(msg))

		self.static_conn.eof()

	def __send_trips(self):
		self.trips_conn = ClientConnection(self.host, self.port_trips)

		for i, city in enumerate(self.cities):
			with open(f'/data/{city}/trips.csv', newline='') as csvfile:
				reader = csv.reader(csvfile, delimiter=',')
				for msg in reader:
					self.trips_conn.send(city, ','.join(msg))
		
		self.trips_conn.eof()
		self.trips_conn.close()
