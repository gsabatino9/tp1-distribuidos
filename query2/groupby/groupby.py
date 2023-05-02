from common.groupby import GroupbyController

def main():
	RECEIVE_QUEUE = "group_by_2"
	SEND_QUEUE = "applier_2"
	EM_QUEUE = "eof_groupby_queue"

	def operation(old, yearid):
		if yearid == '2016':
			return [old[0]+1, old[1]]
		else:
			return [old[0], old[1]+1]
	base_data = [0,0]

	def gen_key_value(msg):
		yearid, name_station = msg.split(',')
		return name_station, yearid

	GroupbyController(RECEIVE_QUEUE, SEND_QUEUE, EM_QUEUE, operation, base_data, gen_key_value)