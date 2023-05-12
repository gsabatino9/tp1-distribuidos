from protocol.message_client import MessageClient
from server.eof_manager.common.message_eof import MessageEOF

def decode(body):
	header, trips_array = MessageClient.decode(body)
	return header, trips_array[0]

def is_eof(body):
	try:
		decode(body)
		return False
	except:
		return True
		
def ack_msg():
	return MessageEOF.ack(MessageEOF.TRIP)