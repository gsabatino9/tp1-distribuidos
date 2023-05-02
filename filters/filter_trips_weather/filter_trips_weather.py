from common.trips_transformer import TripTransformer, TripsTransformer

RECV_QUEUE = "trips_weather_queue"
EM_QUEUE = "eof_filter_queue"

COLUMS_NAMES = """city,start_date,start_station_code,end_date,end_station_code,duration_sec,is_member,yearid,start_prectot,start_qv2m,start_rh2m,start_ps,start_t2m_range,start_ts,start_t2mdew,start_t2mwet,start_t2m_max,end_prectot,end_qv2m,end_rh2m,end_ps,end_t2m_range,end_ts,end_t2mdew,end_t2mwet,end_t2m_max"""
REDUCED_1 = "start_date,duration_sec,start_prectot"
SEND_1 = "group_by_1"

def main():
	t1 = TripTransformer(COLUMS_NAMES, REDUCED_1, {"start_prectot": lambda x: float(x) > 30})
	wanted_queues = [SEND_1]

	transformers = [t1]
	tf = TripsTransformer(RECV_QUEUE, EM_QUEUE, transformers, wanted_queues)