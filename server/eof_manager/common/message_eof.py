from collections import namedtuple
from struct import pack, unpack, calcsize

class MessageEOF:
	# msg type
	EOF = 0
	ACK = 1

	# data type
	STATION = 0
	WEATHER = 1
	TRIP = 2

	HEADER_CODE = '!BB'
	SIZE_HEADER = calcsize(HEADER_CODE)

	Header = namedtuple('Header', 'msg_type data_type')

	def __init__(self, msg_type, data_type):
		self.header = self.Header(msg_type, data_type)

	def encode(self):
		return pack(self.HEADER_CODE, self.header.msg_type, self.header.data_type)

	@classmethod
	def eof(cls, data_type):
		return cls(cls.EOF, data_type).encode()

	@classmethod
	def ack(cls, data_type):
		return cls(cls.ACK, data_type).encode()

	@staticmethod
	def decode(header_bytes):
		return MessageEOF.Header._make(unpack(MessageEOF.HEADER_CODE, header_bytes))