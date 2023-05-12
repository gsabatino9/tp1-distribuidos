from protocol.message_client import MessageClient
from server.eof_manager.message_eof import MessageEOF

def encode_header(header):
	return MessageClient.encode_header(header)

def eof_msg(header):
	return MessageEOF.eof(header.data_type)

def is_station(header):
	return header.data_type == MessageClient.STATION_DATA

def is_weather(header):
	return header.data_type == MessageClient.WEATHER_DATA