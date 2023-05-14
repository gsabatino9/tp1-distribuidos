from applier_query2 import ApplierQuery2
import os

NAME_RECV_QUEUE = os.environ.get("NAME_RECV_QUEUE")
NAME_EM_QUEUE = os.environ.get("NAME_EM_QUEUE")
NAME_SEND_QUEUE = os.environ.get("NAME_SEND_QUEUE")


def main():
    a = ApplierQuery2(NAME_RECV_QUEUE, NAME_EM_QUEUE, NAME_SEND_QUEUE)
    a.stop()


if __name__ == "__main__":
    main()
