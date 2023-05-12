from server.queue.connection import Connection
from server.filters.common.utils import decode
from server.filters.common.filter import Filter

class FilterPretoc:
	def __init__(self, name_recv_exchange, name_recv_queue):
		self.__init_filter()
		self.__connect(name_recv_exchange, name_recv_queue)
		self.recv_queue.receive(self.proccess_message)
		self.queue_connection.start_receiving()

	def __init_filter(self):
		columns_names = """city,start_date,start_station_code,end_date,end_station_code,duration_sec,is_member,yearid,start_prectot,start_qv2m,start_rh2m,start_ps,start_t2m_range,start_ts,start_t2mdew,start_t2mwet,start_t2m_max,end_prectot,end_qv2m,end_rh2m,end_ps,end_t2m_range,end_ts,end_t2mdew,end_t2mwet,end_t2m_max"""
		reduced_columns = "start_date,duration_sec,start_prectot"

		self.filter = Filter(columns_names, reduced_columns, {"start_prectot": lambda x: float(x) > 30})

	def __connect(self, name_recv_exchange, name_recv_queue):
		self.queue_connection = Connection()
		self.recv_queue = self.queue_connection.pubsub_worker_queue(name_recv_exchange, name_recv_queue)

	def proccess_message(self, ch, method, properties, body):
		header, joined_trips = decode(body)
		trips_to_next_stage = []

		for trip in joined_trips:
			new_trip = self.filter.apply(trip)
			if new_trip:
				trips_to_next_stage.append(trip)

		print("Trips next stage:", len(trips_to_next_stage))

	def stop(self):
		self.queue_connection.close()