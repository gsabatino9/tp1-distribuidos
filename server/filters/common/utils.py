from server.eof_manager.common.message_eof import MessageEOF

def ack_msg():
	return MessageEOF.ack(MessageEOF.TRIP)