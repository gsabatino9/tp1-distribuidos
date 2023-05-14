from eof_manager import EOFManager
import os, ast

NAME_RECV_QUEUE = "eof_manager_applier_q"
NAME_APPLIERS_QUEUES = ["applier_query1_q", "applier_query2_q", "applier_query3_q"]
NAME_SEND_QUEUE = "eof_manager_query_result_q"
SIZE_WORKERS = os.environ.get("SIZE_WORKERS")


def main():
    size_workers = ast.literal_eval(SIZE_WORKERS)
    e = EOFManager(NAME_RECV_QUEUE, NAME_APPLIERS_QUEUES, NAME_SEND_QUEUE, size_workers)
    e.stop()


if __name__ == "__main__":
    main()
