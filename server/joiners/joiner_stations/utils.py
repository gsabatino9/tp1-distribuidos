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

class StationsData:
	def __init__(self, idx_code=0, idx_yearid=4, len_msg=5):
		self.stations = {}
		self.idx_code = idx_code
		self.idx_yearid = idx_yearid
		self.idxs_joined_data = []

		for i in range(len_msg):
			if i != idx_code and i != idx_yearid:
				self.idxs_joined_data.append(i)

	def add_station(self, city, station):
		code, yearid = station[self.idx_code], station[self.idx_yearid]
		self.stations[city, code, yearid] = [elem for i,elem in enumerate(station) if i in self.idxs_joined_data]

	def join_trip(self, city, trip):
		"""
		Le retorno: 
		name_start_station, lat_start_station, long_start_station,
		name_end_station, lat_end_station, long_end_station
		"""
		try:
			start_code, end_code, yearid = trip[1], trip[3], trip[6]
			start_station = self.__join_trip(city, start_code, yearid)
			end_station = self.__join_trip(city, end_code, yearid)

			return ','.join(start_station+end_station)
		# poner una excepción propia para catchearla
		except:
			return None

	def __join_trip(self, city, code, yearid):
		return self.stations[city, code, yearid]