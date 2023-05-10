from protocol.message_client import MessageClient

def decode_header(body):
	header = MessageClient.decode_header(body[:MessageClient.SIZE_HEADER])
	payload_bytes = body[MessageClient.SIZE_HEADER:]

	return header, payload_bytes

def is_eof(body):
	try:
		decode_header(body)
		return False
	except:
		return True

def is_station(header):
	return header.data_type == MessageClient.STATION_DATA

def is_weather(header):
	return header.data_type == MessageClient.WEATHER_DATA

def obtain_city(header):
	if header.city == MessageClient.MONTREAL:
		return "montreal"
	elif header.city == MessageClient.TORONTO:
		return "toronto"
	else:
		return "washington"