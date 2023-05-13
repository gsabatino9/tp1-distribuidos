from eof_manager import EOFManager
import os, ast

NAME_RECV_QUEUE = 'eof_manager_filters_q'
NAME_FILTERS_QUEUE = ['filter_pretoc_q', 'filter_year_q', 'filter_distance_q']
NAME_SEND_QUEUE = 'eof_manager_groupby_q'
SIZE_WORKERS = os.environ.get('SIZE_WORKERS')

def main():
	size_workers = ast.literal_eval(SIZE_WORKERS)
	e = EOFManager(NAME_RECV_QUEUE, NAME_FILTERS_QUEUE, NAME_SEND_QUEUE, size_workers)
	e.stop()

if __name__ == "__main__":
	main()