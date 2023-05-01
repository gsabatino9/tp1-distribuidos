from common.eof_manager import EOFManager
import time

NAME_RECV = "eof_groupby_queue"
NAME_NEXT_STAGE = "eof_appliers_queue"

if __name__ == "__main__":
	time.sleep(10)
	EOFManager(NAME_RECV, NAME_NEXT_STAGE)