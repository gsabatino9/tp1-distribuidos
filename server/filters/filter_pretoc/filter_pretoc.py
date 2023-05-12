from server.queue.connection import Connection
from server.filters.common.utils import decode, is_eof, ack_msg, construct_msg
from server.filters.common.filter import Filter

class FilterPretoc:
	def __init__(self, name_recv_exchange, name_recv_queue, name_em_queue, name_send_queue):
		self.not_filtered = 0
		self.__init_filter()
		self.__connect(name_recv_exchange, name_recv_queue, name_em_queue, name_send_queue)
		self.recv_queue.receive(self.proccess_message)
		self.queue_connection.start_receiving()

	def __init_filter(self):
		columns_names = """start_date,start_station_code,end_date,end_station_code,duration_sec,is_member,yearid,start_prectot,start_qv2m,start_rh2m,start_ps,start_t2m_range,start_ts,start_t2mdew,start_t2mwet,start_t2m_max,end_prectot,end_qv2m,end_rh2m,end_ps,end_t2m_range,end_ts,end_t2mdew,end_t2mwet,end_t2m_max"""
		reduced_columns = "start_date,duration_sec,start_prectot"

		self.filter = Filter(columns_names, reduced_columns, {"start_prectot": lambda x: float(x) > 0.01})

	def __connect(self, name_recv_exchange, name_recv_queue, name_em_queue, name_send_queue):
		self.queue_connection = Connection()
		self.recv_queue = self.queue_connection.pubsub_worker_queue(name_recv_exchange, name_recv_queue)
		self.em_queue = self.queue_connection.pubsub_queue(name_em_queue)
		self.send_queue = self.queue_connection.basic_queue(name_send_queue)

	def proccess_message(self, ch, method, properties, body):
		if is_eof(body):
			self.__eof_arrived(ch)
		else:
			self.__filter(body)

	def __filter(self, body):
		header, joined_trips = decode(body)
		trips_to_next_stage = []

		for trip in joined_trips:
			new_trip = self.filter.apply(trip)
			if new_trip:
				self.not_filtered += 1
				trips_to_next_stage.append(new_trip)

		self.__send_next_stage(header, trips_to_next_stage)

	def __send_next_stage(self, header, trips_to_next_stage):
		if len(trips_to_next_stage) > 0:
			msg = construct_msg(header, trips_to_next_stage)
			self.send_queue.send(msg)

	def __eof_arrived(self, ch):
		ch.stop_consuming()
		print("EOF llegó a filtro - not_filtered", self.not_filtered)
		self.em_queue.send(ack_msg())

	def stop(self):
		self.queue_connection.close()