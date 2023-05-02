def decode(msg):
	return msg.decode('utf-8')

def split_city(msg, splitted=False):
	if not splitted:
		msg = msg.split(',')

	city = msg[0]
	data = msg[1:]

	return city, data