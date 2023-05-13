from eof_manager import EOFManager
import os

NAME_RECV_QUEUE = 'eof_manager_query_result_q'
NAME_VERIFIER_QUEUE = 'query_results_q'
SIZE_QUERIES = 3

def main():
	e = EOFManager(NAME_RECV_QUEUE, NAME_VERIFIER_QUEUE, SIZE_QUERIES)
	e.stop()

if __name__ == "__main__":
	main()