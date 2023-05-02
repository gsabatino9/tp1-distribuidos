from common.connection import Connection
from common.eof_manager import EOF_MSG, WORKER_DONE_MSG
from common.utils import *

class FilterColumns:
	def __init__(self, columns, wanted_columns):
		columns = columns.split(',')
		wanted_columns = wanted_columns.split(',')
		
		self.idxs = [i for i, col in enumerate(columns) if col in wanted_columns]

	def __obtain_idxs(self):
		return [i for i, col in enumerate(self.columns) if col in self.wanted_columns]
	
	def filter(self, columns):
		columns = columns.split(",")
		result = []
	
		for i, col in enumerate(columns):
			if i in self.idxs:
				result.append(col)
				
		return ','.join(result)

class FilterRows:
	def __init__(self, columns, dict_cond):
		keys = columns.split(",")
		new_dict = {}
		for i, key in enumerate(keys):
				if key in dict_cond:
						new_dict[i] = dict_cond[key]

		self.conditions = self.__map_conditions(len(keys), new_dict)

	def __map_conditions(self, max_args, dict_cond):
		conditions = []
		for i in dict_cond:
			conditions = self.__fill_conds(conditions, i)
			conditions.append(dict_cond[i])
		
		return conditions
				
	def __fill_conds(self, conds, next):
		diff_cons = next - len(conds)
		for i in range(len(conds), diff_cons):
			conds.append(True)

		return conds
	
	def filter(self, row):
		elements = row.split(",")
		result = []
		for elem, condition in zip(elements, self.conditions):
			if callable(condition):
				if not condition(elem):
					return None
		return row

class Filter:
	def __init__(self, columns_names, wanted_columns, filter_conditions):
		self.filter_columns = FilterColumns(columns_names, wanted_columns)
		self.filter_rows = FilterRows(wanted_columns, filter_conditions)

	def apply(self, trip):
		transf_trip = self.filter_columns.filter(trip)
		
		if self.filter_rows.filter(transf_trip):
			return transf_trip
		else: return None

class FilterController:
	def __init__(self, recv_queue, em_queue, transformers, send_queues):
		self.transformers = transformers
		self.__connect(recv_queue, em_queue, send_queues)

		print("[trips_transformer] listo para recibir")
		self.connection.start_receiving()

	def __connect(self, recv_queue, em_queue, send_queues):
		self.connection = Connection()
		self.recv_queue = self.connection.basic_queue(recv_queue)
		self.recv_queue.receive(self.recv_trip, auto_ack=False)
		self.queues = []

		for send_queue in send_queues:
			queue = self.connection.basic_queue(send_queue)
			self.queues.append(queue)

		self.__connect_to_eof_manager(em_queue, recv_queue)

	def __connect_to_eof_manager(self, em_queue, recv_queue):
		self.em_queue = self.connection.pubsub_queue(em_queue)
		self.em_queue.send(recv_queue) # le digo de dónde espero el eof

	def __check_eof(self, msg, ch, delivery_tag):
		if msg == EOF_MSG:
			self.connection.stop_receiving()
			self.em_queue.send(WORKER_DONE_MSG)
			ch.basic_ack(delivery_tag=delivery_tag)
			return True
		
		return False

	def recv_trip(self, ch, method, properties, body):
		trip = decode(body)

		if self.__check_eof(trip, ch, method.delivery_tag): return
		
		for i, transformer in enumerate(self.transformers):
			transf_trip = transformer.apply(trip)
			if transf_trip:
				self.queues[i].send(transf_trip)
				print(transf_trip)
		ch.basic_ack(delivery_tag=method.delivery_tag)

	def close(self):
		print('close: success')
		self.connection.close()

