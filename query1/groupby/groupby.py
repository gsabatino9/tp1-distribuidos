from common.groupby import GroupbyController

def main():
	RECEIVE_QUEUE = "group_by_1"
	SEND_QUEUE = "applier_1"
	EM_QUEUE = "eof_groupby_queue"

	operation = lambda old, new: [old[0]+max(new,0), old[1]+1]
	base_data = [0,0]

	def gen_key_value(msg):
		start_date, duration_sec, start_pretoc = msg.split(',')
		return start_date, float(duration_sec)

	GroupbyController(RECEIVE_QUEUE, SEND_QUEUE, EM_QUEUE, operation, base_data, gen_key_value)