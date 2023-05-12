from collections import namedtuple
from struct import pack, unpack, calcsize

class Message:
	# Struct format for message header
	HEADER_CODE = '!BI'
	# Size of header in bytes
	SIZE_HEADER = calcsize(HEADER_CODE)

	# Define the named tuples used in the protocol
	Header = namedtuple('Header', 'num_query len')
	Payload = namedtuple('Payload', 'data')

	def __init__(self, num_query, payload):
		if payload is None:
			payload = []
		payload_bytes = self._pack_payload(payload)

		self.header = self.Header(num_query, len(payload_bytes))
		self.payload = self.Payload(payload_bytes)

	def encode(self):
		header = self.encode_header(self.header)
		payload = self.encode_payload(self.header.len, self.payload)

		return header+payload

	@staticmethod
	def encode_header(header):
		return pack(Message.HEADER_CODE, header.num_query, header.len)

	@staticmethod
	def encode_payload(len_payload, payload):
		return pack(f'!{len_payload}s', payload.data)

	@staticmethod
	def decode(msg):
		header = Message.decode_header(msg[:Message.SIZE_HEADER])
		payload = Message.decode_payload(msg[Message.SIZE_HEADER:])

		return header, payload

	@staticmethod
	def decode_header(header):
		return Message.Header._make(unpack(Message.HEADER_CODE, header))

	@staticmethod
	def decode_payload(payload_bytes):
		return Message._unpack_payload(payload_bytes)

	@staticmethod
	def _pack_payload(payload):
		payload_str = '\0'.join(payload)
		return payload_str.encode('utf-8')

	@staticmethod
	def _unpack_payload(payload_bytes):
		payload = payload_bytes.decode('utf-8').split('\0')
		return Message.Payload(payload)	