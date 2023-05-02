from common.filter import Filter, FilterController

RECV_QUEUE = "trips_stations_queue"
EM_QUEUE = "eof_filter_queue"

COLUMS_NAMES = """city,start_date,start_station_code,end_date,end_station_code,duration_sec,is_member,yearid,name_start_station,lat_start_station,long_start_station,name_end_station,lat_end_station,long_end_station"""
REDUCED_1 = "yearid,name_start_station"
REDUCED_2 = "city,lat_start_station,long_start_station,name_end_station,lat_end_station,long_end_station"
SEND_1 = "group_by_2"
SEND_2 = "group_by_3"

def main():
	f1 = Filter(COLUMS_NAMES, REDUCED_1, {"yearid": lambda x: int(x) in [2016, 2017]})
	f2 = Filter(COLUMS_NAMES, REDUCED_2, {"city": lambda x: x == "Montreal"})
	FilterController(RECV_QUEUE, EM_QUEUE, [f1, f2], [SEND_1, SEND_2])