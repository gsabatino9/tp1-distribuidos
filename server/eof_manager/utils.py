from message_eof import MessageEOF

def decode(header_bytes):
	return MessageEOF.decode(header_bytes)

def is_eof(header):
	return header.msg_type == MessageEOF.EOF