from common.groupby import Groupby
from common.connection import Connection
from common.eof_manager import EOF_MSG, WORKER_DONE_MSG
from common.utils import *
from haversine import haversine

def main():
	conn = Connection()
	RECEIVE_QUEUE = "group_by_3"
	SEND_QUEUE = "applier_3"
	EM_QUEUE = "eof_groupby_queue"

	operation = lambda old, new: [old[0]+new, old[1]+1]
	base_data = [0,0]
	g = Groupby(operation, base_data)

	recv_queue = conn.basic_queue(RECEIVE_QUEUE)
	em_queue = conn.pubsub_queue(EM_QUEUE)
	em_queue.send(RECEIVE_QUEUE)

	send_queue = conn.basic_queue(SEND_QUEUE)

	def callback(ch, method, properties, body):
		"""
		Llega con:
		yearid,name_start_station
		"""
		msg = decode(body)

		if msg == EOF_MSG:
			__eof_arrived()
		else:
			__data_arrived(msg)

	def __eof_arrived():
		print('EOF arrived')
		for station in g.grouped_data:
			value = g.grouped_data[station]
			msg = station + ',' + str(value[0]) + ',' + str(value[1])
			send_queue.send(msg)

		conn.stop_receiving()
		em_queue.send(WORKER_DONE_MSG)

	def __data_arrived(msg):
		city,name_end_station,lat_start_station,long_start_station,lat_end_station,long_end_station = msg.split(',')
		distance = haversine(float(lat_start_station), float(long_start_station), float(lat_end_station), float(long_end_station))

		g.add_data(name_end_station, distance)

	recv_queue.receive(callback)
	conn.start_receiving()

	conn.close()
