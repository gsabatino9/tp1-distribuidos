import socket, pika, struct, random
from queue import Queue

HOST = 'localhost'
PORT = 12345

STATIONS_QUEUE = "stations_queue"
TRIPS_QUEUE = "trips_queue"

def receive(connection):
	data = connection.recv(4)
	message_size = struct.unpack('I', data)[0]
	return recv_all(connection, message_size)

def recv_all(connection, message_size):
	chunks = []
	bytes_received = 0
	while bytes_received < message_size:
		chunk = connection.recv(min(message_size - bytes_received, 1024))
		if not chunk:
			break
		chunks.append(chunk)
		bytes_received += len(chunk)

	return b''.join(chunks)

queue = Queue()
queue.add_queues([STATIONS_QUEUE, TRIPS_QUEUE])

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
	sock.bind((HOST, PORT))
	sock.listen()

	print(f"Servidor escuchando en {HOST}:{PORT}")
	conn, addr = sock.accept()
	with conn:
		print(f"Conexión aceptada desde {addr}")

		data = receive(conn)
		try:
			while data:
				queue.send(STATIONS_QUEUE, data)
				data = receive(conn)
		except:
			print("Algo rompió, received")

		print("Conexión cerrada")
		conn.close()

	queue.send(STATIONS_QUEUE, b'last')
	queue.send(TRIPS_QUEUE, bytes("""2014-06-01 00:00:00,6209,2014-06-01 00:28:00,6210,1680.0,0,2014""", 
									"utf-8"))
	queue.close()
