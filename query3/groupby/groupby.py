from common.groupby import GroupbyController
from haversine import haversine

def main():
	RECEIVE_QUEUE = "group_by_3"
	SEND_QUEUE = "applier_3"
	EM_QUEUE = "eof_groupby_queue"

	operation = lambda old, new: [old[0]+new, old[1]+1]
	base_data = [0,0]

	def gen_key_value(msg):
		print(msg)
		city,lat_start_station,long_start_station,name_end_station,lat_end_station,long_end_station = msg.split(',')
		distance = haversine((float(lat_start_station), float(long_start_station)), (float(lat_end_station), float(long_end_station)))

		return name_end_station, distance

	GroupbyController(RECEIVE_QUEUE, SEND_QUEUE, EM_QUEUE, operation, base_data, gen_key_value)