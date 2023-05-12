from protocol.message_client import MessageClient
from server.eof_manager.common.message_eof import MessageEOF

def eof_msg(header):
	return MessageEOF.eof(header.data_type)

def is_eof(header):
	return header.msg_type == MessageClient.SEND_LAST