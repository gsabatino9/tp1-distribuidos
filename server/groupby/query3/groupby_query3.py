from server.groupby.common.groupby_controller import GroupbyController

class GroupbyQuery3:
	def __init__(self, name_recv_queue, name_em_queue, name_send_queue):
		operation = lambda old, new: [old[0]+new, old[1]+1]
		base_data = [0,0]

		self.groupby_controller = GroupbyController(name_recv_queue, name_em_queue, name_send_queue, operation, base_data, self.gen_key_value)

	def gen_key_value(self, trip):
		return trip[0], float(trip[1])

	def gen_key_value(msg):
		print(msg)
		city,lat_start_station,long_start_station,name_end_station,lat_end_station,long_end_station = msg.split(',')
		distance = haversine((float(lat_start_station), float(long_start_station)), (float(lat_end_station), float(long_end_station)))

		return name_end_station, distance

	def stop(self):
		self.groupby_controller.stop()