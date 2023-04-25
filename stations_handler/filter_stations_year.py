import pika, sys, os
from filter import FilterColumns, FilterRows

COLUMS_NAMES = "code,name,latitude,longitude,yearid"
FILTERED_COLUMNS = "code,name,yearid"
LEN_ROW = len(FILTERED_COLUMNS.split(','))
RECEIVE_QUEUE = "stations_queue"
NEXT_STAGE_QUEUE = "join_stations_trips"

class FilterStationsByYear:
	def __init__(self, years):
		self.__connect()
		self.filter_columns = FilterColumns(COLUMS_NAMES)
		self.filter_rows = FilterRows(LEN_ROW, {2: lambda x: int(x) in years})

	def __connect(self):
		self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1'))
		self.channel = self.connection.channel()

		# receive queues
		self.channel.queue_declare(queue=RECEIVE_QUEUE)

		# next stage queues
		self.channel.queue_declare(queue=NEXT_STAGE_QUEUE)

	def start_receiving(self):
		self.channel.basic_consume(queue=RECEIVE_QUEUE,
							  auto_ack=True,
							  on_message_callback=self.filter_callback)

		print('[FilterStationsByYear] Waiting for messages.')
		self.channel.start_consuming()

	def filter_callback(self, ch, method, properties, body):
		row = self.filter_columns.filter(FILTERED_COLUMNS, body)
		if not self.filter_rows.filter(row):
			# pasa a siguiente etapa
			self.__send_next_stage(row)

	def __send_next_stage(self, row):
		print(f'Pasa a siguiente etapa: {row}')
		# acá va la parte de mandar a las queues de la siguiente etapa
		# (que solo conoce eso)
		channel.basic_publish(
			exchange='',
			routing_key=NEXT_STAGE_QUEUE,
			body=row
		)

	def end(self):
		print('[FilterStationsByYear] fin')

