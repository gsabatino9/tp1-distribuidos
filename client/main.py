import socket, struct, time
import data.Montreal, data.Washington, data.Toronto
from protocol.client_protocol import ClientConnection

HOST = 'receiver'
PORT_STATIC = 12345
PORT_TRIPS = 12346

def main():
	static_conn = ClientConnection(HOST, PORT_STATIC)
	cities = [data.Montreal.stations, data.Toronto.stations, data.Washington.stations]

	for i, city in enumerate(["Montreal", "Toronto", "Washington"]):
		stations = cities[i]
		for msg in stations:
			static_conn.send(city, msg)

	static_conn.eof()

	cities = [data.Montreal.weathers, data.Toronto.weathers, data.Washington.weathers]
	for i, city in enumerate(["Montreal", "Toronto", "Washington"]):
		weather = cities[i]
		for msg in weather:
			static_conn.send(city, msg)

	static_conn.eof()

	static_conn.close()

	time.sleep(3)

	trips_conn = ClientConnection(HOST, PORT_TRIPS)
	cities = [data.Montreal.trips, data.Toronto.trips, data.Washington.trips]

	for i, city in enumerate(["Montreal", "Toronto", "Washington"]):
		trips = cities[i]
		for msg in trips:
			trips_conn.send(city, msg)
	
	trips_conn.eof()
	trips_conn.close()

if __name__ == "__main__":
	time.sleep(11)
	main()