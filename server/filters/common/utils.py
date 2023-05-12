from protocol.message_client import MessageClient

def decode(body):
	header, trips_array = MessageClient.decode(body)
	return header, trips_array[0]