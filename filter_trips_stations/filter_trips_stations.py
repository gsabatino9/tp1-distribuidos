from common.trips_transformer import TripTransformer, TripsTransformer

RECV_QUEUE = "trips_stations_queue"

COLUMS_NAMES = """start_date,start_station_code,end_date,end_station_code,duration_sec,is_member,yearid,name_start_station,lat_start_station,long_start_station,name_end_station,lat_end_station,long_end_station"""
REDUCED_1 = "yearid,name_start_station"
SEND_1 = "group_by_2"

def main():
	t1 = TripTransformer(COLUMS_NAMES, REDUCED_1, {"yearid": lambda x: int(x) in [2016, 2017]})
	wanted_queues = [SEND_1]

	transformers = [t1]
	tf = TripsTransformer(RECV_QUEUE, transformers, wanted_queues)