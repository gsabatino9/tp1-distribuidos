import socket, struct, time
import data.Montreal, data.Washington, data.Toronto

HOST = 'receiver'
PORT_STATIC = 12345
PORT_TRIPS = 12346

def main():
	static_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	static_socket.connect((HOST, PORT_STATIC))
	cities = [data.Montreal.stations, data.Toronto.stations, data.Washington.stations]

	for i, city in enumerate(["Montreal", "Toronto", "Washington"]):
		stations = cities[i]
		for msg in stations:
			msg = city + "," + msg
			bytes_msg = bytes(msg, 'utf-8')
			len_msg = len(bytes_msg)

			static_socket.sendall(struct.pack('!i', len_msg))
			static_socket.sendall(bytes_msg)

	static_socket.sendall(struct.pack('!i', len(b'EOF')))
	static_socket.sendall(b'EOF')

	static_socket.close()

	time.sleep(3)

	trips_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	trips_socket.connect((HOST, PORT_TRIPS))

	cities = [data.Montreal.trips, data.Toronto.trips, data.Washington.trips]

	for i, city in enumerate(["Montreal", "Toronto", "Washington"]):
		trips = cities[i]
		for msg in trips:
			msg = city + "," + msg
			bytes_msg = bytes(msg, 'utf-8')
			len_msg = len(bytes_msg)

			trips_socket.sendall(struct.pack('!i', len_msg))
			trips_socket.send(bytes_msg)
	
	trips_socket.sendall(struct.pack('!i', len(b'EOF')))
	trips_socket.sendall(b'EOF')

	trips_socket.close()

if __name__ == "__main__":
	time.sleep(11)
	main()