from common.trips_transformer import TripTransformer, TripsTransformer

RECV_QUEUE = "trips_stations_queue"
EM_QUEUE = "eof_filter_queue"

COLUMS_NAMES = """city,start_date,start_station_code,end_date,end_station_code,duration_sec,is_member,yearid,name_start_station,lat_start_station,long_start_station,name_end_station,lat_end_station,long_end_station"""
REDUCED_1 = "yearid,name_start_station"
REDUCED_2 = "city,name_end_station,lat_start_station,long_start_station,lat_end_station,long_end_station"
SEND_1 = "group_by_2"
SEND_2 = "group_by_3"

def main():
	t1 = TripTransformer(COLUMS_NAMES, REDUCED_1, {"yearid": lambda x: int(x) in [2016, 2017]})
	t2 = TripTransformer(COLUMS_NAMES, REDUCED_2, {"city": lambda x: x == "Montreal"})
	wanted_queues = [SEND_1, SEND_2]

	transformers = [t1]
	tf = TripsTransformer(RECV_QUEUE, EM_QUEUE, transformers, wanted_queues)