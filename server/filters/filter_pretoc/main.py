from filter_pretoc import FilterPretoc

NAME_RECV_EXCHANGE = "filter_joined_weather_q"
NAME_RECV_QUEUE = "filter_pretoc_q"
NAME_EM_QUEUE = "eof_manager_filters_q"
NAME_SEND_QUEUE = "groupby_query1_q"


def main():
    f = FilterPretoc(
        NAME_RECV_EXCHANGE, NAME_RECV_QUEUE, NAME_EM_QUEUE, NAME_SEND_QUEUE
    )
    f.stop()


if __name__ == "__main__":
    main()
