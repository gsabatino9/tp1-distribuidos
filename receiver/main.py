import socket, pika, struct, random

HOST = 'localhost'
PORT = 12345

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

connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1'))
channel = connection.channel()

channel.queue_declare(queue='stations_queue')
channel.queue_declare(queue='eof_queue')

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
				print('sending')
				channel.basic_publish(exchange='',
					routing_key='stations_queue',
					body=data)

				data = receive(conn)
		except:
			print("Algo rompió, received")

		print("Conexión cerrada")
		conn.close()
	channel.basic_publish(exchange='',
				  routing_key='eof_queue',
				  body='')

	connection.close()
