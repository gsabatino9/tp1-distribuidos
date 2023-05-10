import socket

class Communication:
	def __init__(self, socket):
		self.socket = socket

	def getpeername(self):
		return self.socket.getpeername()

	def send_message(self, msg):
		self.socket.sendall(msg)

	def recv_header(self, len_header):
		header_bytes = self.socket.recv(len_header)
		return header_bytes

	def recv_payload(self, len_payload):
		buffer = bytearray()

		while len(buffer) < len_payload:
			data = self.socket.recv(len_payload-len(buffer))
			if not data:
				raise ConnectionError("Socket cerrado inesperadamente.")
			buffer += data

		return bytes(buffer)

	def stop(self):
		"""
		Function to release server resources.

		The server closes the socket file descriptor and 
		logs the action at the start and end of the operation.
		"""
		try:
			self.socket.shutdown(socket.SHUT_RDWR)
			self.socket.close()
		except:
			print('Socket ya desconectado')