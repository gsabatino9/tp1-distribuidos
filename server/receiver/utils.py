from protocol.message_client import MessageClient
from server.eof_manager.message_eof import MessageEOF

def encode_header(header):
	return MessageClient.encode_header(header)

def eof_msg(header):
	return MessageEOF.eof(header.data_type)
