from eof_manager import EOFManager
import os

NAME_RECV_QUEUE = 'eof_manager_filters_q'
NAME_FILTERS_QUEUE = 'filter_pretoc_q'
SIZE_WORKERS = os.environ.get('SIZE_WORKERS')

def main():
	size_workers = [int(i) for i in SIZE_WORKERS]
	e = EOFManager(NAME_RECV_QUEUE, NAME_FILTERS_QUEUE, size_workers)
	e.stop()

if __name__ == "__main__":
	main()