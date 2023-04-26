from queue import Queue
import sys, os

RECEIVE_QUEUE = "stations_queue"
TRIPS_QUEUE = "trips_queue"
NEXT_STAGE_QUEUE = "joined_stations_queue"
EOF_MSG = "last"

class StationsHandler:
	def __init__(self):
		self.stations = {}
		
		names_queues = [RECEIVE_QUEUE, TRIPS_QUEUE, NEXT_STAGE_QUEUE]

		self.queue = Queue()
		self.queue.add_queues(names_queues)
		self.queue.add_callback(RECEIVE_QUEUE, self.proccess_message)
		
		self.queue.start_receiving()

	def proccess_message(self, ch, method, properties, body):
		if body.decode() == EOF_MSG:
			self.__eof_arrived()
		else:
			self.__station_arrived(body)

	def __station_arrived(self, msg):
		station = msg.decode('utf-8').split(',')
		self.stations[station[0], station[-1]] = msg

	def __eof_arrived(self):
		self.queue.add_callback(TRIPS_QUEUE, self.join_trip)
		#self.queue.close()

	# entro acá solo si terminé de procesar los Stations.
	def join_trip(self, ch, method, properties, body):
		trip = body.decode('utf-8').split(',')
		station_trip = self.stations[trip[1], trip[-1]]
		if not station_trip: print('Error')
		else:
			print('Mandando a siguiente etapa')
			self.queue.send(NEXT_STAGE_QUEUE, station_trip)

		self.queue.close()

