import socket
from struct import pack
from protocol.constants import EOF_MSG, HEADER


class ClientConnection:
	def __init__(self, host, port):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.connect((host, port))

	def send(self, city, msg):
		bytes_msg = self.__generate_msg(city, msg)
		self.socket.sendall(bytes_msg)

	def eof(self):
		len_msg = self.__len_msg(EOF_MSG)
		self.socket.sendall(len_msg+EOF_MSG)

	def __generate_msg(self, city, msg):
		bytes_msg = self.__bytes_msg(city, msg)
		len_msg = self.__len_msg(bytes_msg)

		return len_msg + bytes_msg

	def __bytes_msg(self, city, msg):
		msg = city + "," + msg
		return bytes(msg, 'utf-8')

	def __len_msg(self, msg):
		return pack(HEADER, len(msg))

	def close(self):
		self.socket.close()
