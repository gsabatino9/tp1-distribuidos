from query_state_verifier import QueryStateVerifier
import time

def main():
	EM_QUEUE = "eof_query_result_queue"
	RECEIVE_QUEUE = "query_result_queue"
	queries = ["query1", "query2", "query3"]

	QueryStateVerifier(RECEIVE_QUEUE, EM_QUEUE, queries)

if __name__ == "__main__":
	time.sleep(10)
	main()