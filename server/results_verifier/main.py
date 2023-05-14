from results_verifier import ResultsVerifier

HOST = "results_verifier"
PORT = 12346
NAME_RECV_QUEUE = "query_results_q"
NAME_EM_QUEUE = "eof_manager_query_result_q"


def main():
    f = ResultsVerifier(NAME_RECV_QUEUE, NAME_EM_QUEUE, HOST, PORT)
    f.stop()


if __name__ == "__main__":
    main()
