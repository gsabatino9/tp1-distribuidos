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

def obtain_city(header):
	if header.city == MessageClient.MONTREAL:
		return "montreal"
	elif header.city == MessageClient.TORONTO:
		return "toronto"
	else:
		return "washington"

def ack_msg():
	return MessageEOF.ack(MessageEOF.TRIP)

def construct_msg(header, joined_trips):
	return MessageClient(header.data_type, header.msg_type, header.city, joined_trips).encode()

class WeatherData:
	def __init__(self, idx_date=0, len_msg=10):
		self.weathers = {}
		self.idx_date = idx_date
		self.idxs_joined_data = []

		for i in range(len_msg):
			if i != idx_date:
				self.idxs_joined_data.append(i)

	def add_weather(self, city, weather):
		idx_date = weather[self.idx_date]
		self.weathers[city, idx_date] = [elem for i,elem in enumerate(weather) if i in self.idxs_joined_data]

	def join_trip(self, city, trip):
		try:
			start_date, end_date = trip[0], trip[2]
			start_weather = self.__join_trip(city, start_date)
			end_weather = self.__join_trip(city, end_date)

			return ','.join(trip+start_weather+end_weather)
		# poner una excepción propia para catchearla
		except:
			return None

	def __join_trip(self, city, date):
		return self.weathers[city, date]