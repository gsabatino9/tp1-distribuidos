from results_verifier import ResultsVerifier

NAME_RECV_QUEUE = 'query_results_q'
NAME_EM_QUEUE = 'eof_manager_query_result_q'

def main():
	f = ResultsVerifier(NAME_RECV_QUEUE, NAME_EM_QUEUE)
	f.stop()

if __name__ == "__main__":
	main()