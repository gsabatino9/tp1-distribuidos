import socket
from struct import unpack
from protocol.constants import LEN_HEADER, HEADER

class ServerProtocol:
	def __init__(self, host, port):
		self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server_socket.bind((host, port))
		self.server_socket.listen()

	def connect_client(self):
		client_socket, addr = self.server_socket.accept()
		self.socket = client_socket

	def recv(self):
		len_msg = self.__recv_len_msg()
		msg = self.__recv_all(len_msg)

		return msg

	def __recv_len_msg(self):
		data = self.socket.recv(LEN_HEADER)
		return unpack(HEADER, data)[0]

	def __recv_all(self, len_msg):
		buffer = bytearray()

		while len(buffer) < len_msg:
			data = self.socket.recv(len_msg-len(buffer))
			if not data:
				raise ConnectionError("Socket cerrado inesperadamente.")
			buffer += data

		return bytes(buffer)

	def close(self):
		self.socket.close()
		self.server_socket.close()