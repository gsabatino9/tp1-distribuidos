from common.groupby import Groupby
from common.connection import Connection
from common.eof_manager import EOFManager

def main():
	conn = Connection()
	RECEIVE_QUEUE = "group_by_2"
	SEND_QUEUE = "applier_2"

	#operation = lambda old, new: [old[0]+new, old[1]+1]
	def operation(old, yearid):
		if yearid == '2016':
			return [old[0]+1, old[1]]
		else:
			return [old[0], old[1]+1]

	base_data = [0,0]
	g = Groupby(operation, base_data)

	em = EOFManager([])
	send_queue = conn.basic_queue(SEND_QUEUE)

	def callback(ch, method, properties, body):
		"""
		Llega con:
		yearid,name_start_station
		"""
		msg = body.decode('utf-8')
		if em.is_eof(msg):
			if em.all_eof_received():
				for station in g.grouped_data:
					value = g.grouped_data[station]
					msg = station + ',' + str(value[0]) + ',' + str(value[1])
					send_queue.send(msg)
		else:
			yearid, name_station = msg.split(',')

			g.add_data(name_station, yearid)
			print('Data agrupada: \n\t', g.grouped_data)


	recv_queue = conn.basic_queue(RECEIVE_QUEUE)
	recv_queue.receive(callback)
	conn.start_receiving()

	conn.close()
