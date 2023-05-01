from common.trips_transformer import TripTransformer, TripsTransformer

RECV_QUEUE = "trips_queue"
EM_QUEUE = "eof_filter_queue"

COLUMS_NAMES = "start_date,start_station_code,end_date,end_station_code,duration_sec,is_member,yearid"
REDUCED_1 = "duration_sec,yearid"
REDUCED_2 = "start_date,is_member,yearid"
SEND_1 = "group_by_1"
SEND_2 = "group_by_3"

def main():
	#t1 = TripTransformer(COLUMS_NAMES, REDUCED_1, {"is_member": lambda x: int(x) == 0})
	t2 = TripTransformer(COLUMS_NAMES, REDUCED_2, {"yearid": lambda x: int(x) in [2016, 2017]})
	wanted_queues = [SEND_2]

	transformers = [t2]
	tf = TripsTransformer(RECV_QUEUE, EM_QUEUE, transformers, wanted_queues)
	