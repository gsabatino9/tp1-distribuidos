from eof_manager import EOFManager
import os

NAME_RECV_QUEUE = 'eof_manager_filters_q'
NAME_FILTERS_QUEUE = 'filter_pretoc_q'
SIZE_WORKERS = int(os.environ.get('SIZE_WORKERS'))

def main():
	e = EOFManager(NAME_RECV_QUEUE, NAME_FILTERS_QUEUE, SIZE_WORKERS)
	e.stop()

if __name__ == "__main__":
	main()