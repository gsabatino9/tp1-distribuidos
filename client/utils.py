from protocol.message_client import MessageClient

def construct_city(city):
	if city == "montreal":
		return MessageClient.MONTREAL
	elif city == "toronto":
		return MessageClient.TORONTO
	else:
		return MessageClient.WASHINGTON

def construct_payload(rows):
	return [','.join(e) for e in rows]