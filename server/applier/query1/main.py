from applier_query1 import ApplierQuery1
import os

NAME_RECV_QUEUE = "applier_query1_q"
NAME_EM_QUEUE = "eof_manager_applier_q"
NAME_SEND_QUEUE = "query_results_q"


def main():
    a = ApplierQuery1(NAME_RECV_QUEUE, NAME_EM_QUEUE, NAME_SEND_QUEUE)
    a.stop()


if __name__ == "__main__":
    main()
