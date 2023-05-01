import csv, socket, struct

HOST = 'server'
PORT = 12345

with open('stations.csv', 'r') as csv_file:
	csv_reader = csv.reader(csv_file)
	
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
		sock.connect((HOST, PORT))
		print("Conexión establecida")
		
		for row in csv_reader:
			if row[0] == "code": continue
			message = ','.join(row).encode('utf-8')
			message_size = struct.pack('I', len(message))

			sock.sendall(message_size)
			sock.sendall(message)

		sock.close()

	print("Todo mandado")
