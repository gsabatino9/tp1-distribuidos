from protocol.communication_client import CommunicationClient
from utils import construct_payload, construct_city
import csv, socket, threading
from itertools import islice
from datetime import datetime

class Client:
	def __init__(self, host, port, chunk_size):
		self.chunk_size = chunk_size
		# try-except
		skt = self.__connect(host, port)
		self.conn = CommunicationClient(skt)
		print(f"[cliente] conectado {self.conn.getpeername()}")

	def __connect(self, host, port):
		client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client_socket.connect((host, port))
		return client_socket

	def run(self, filepaths, types_files, cities):
		threads = []

		for file in types_files:
			self.__send_type_file(filepaths, file, cities)
			"""t = threading.Thread(target=self.__send_type_file, args=(filepaths, file, cities))
			threads.append(t)
			t.start()

		for t in threads:
			t.join()"""

		print("Esperando confirmación archivos.")
		self.conn.recv_files_received()
		print("Todos los archivos enviados correctamente al servidor.")

	# manda todo de una stations, weather o trips
	def __send_type_file(self, filepaths, type_file, cities):
		send_data = 0
		for i, filepath in enumerate(filepaths):
			with open(filepath + type_file + '.csv', newline='') as csvfile:
				reader = csv.reader(csvfile, delimiter=',')
				
				# skip header
				next(reader)
				last_chunk = False
				while True:
					chunk = list(islice(reader, self.chunk_size))
					if not chunk: break
					chunk = self.__preprocess_chunk(type_file, chunk)
					self.__send_chunk(type_file, chunk, cities[i], False)
					send_data += 1

		self.__send_chunk(type_file, list(''), cities[i], True)
		print(f"[cliente_{type_file}] cantidad enviada: {send_data}")

	def __send_chunk(self, data_type, chunk, city, last_chunk):
		city = construct_city(city)
		payload = construct_payload(chunk)
		self.conn.send(data_type, payload, city, last_chunk)

	def __preprocess_chunk(self, type_file,chunk):
		if type_file != "trips": return chunk
		for row in chunk:
			start_date = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')
			end_date = datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S')
			row[0] = start_date.strftime('%Y-%m-%d')
			row[2] = end_date.strftime('%Y-%m-%d')

		return chunk

	def stop(self):
		self.conn.stop()