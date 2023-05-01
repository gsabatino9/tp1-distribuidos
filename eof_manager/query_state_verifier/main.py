from eof_manager.eof_manager import EOFManager
import time

NAME_RECV = "eof_query_result_queue"

if __name__ == "__main__":
	time.sleep(10)
	EOFManager(NAME_RECV, None)