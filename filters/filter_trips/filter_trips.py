from common.filter import Filter, FilterController

RECV_QUEUE = "trips_queue"
EM_QUEUE = "eof_filter_queue"

COLUMS_NAMES = "city,start_date,start_station_code,end_date,end_station_code,duration_sec,is_member,yearid"
REDUCED_2 = "start_date,is_member,yearid"
SEND_2 = "group_by_4"

def main():
	f = Filter(COLUMS_NAMES, REDUCED_2, {"yearid": lambda x: int(x) in [2016, 2017]})
	FilterController(RECV_QUEUE, EM_QUEUE, [f], [SEND_2])
	