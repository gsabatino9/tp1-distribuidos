from protocol.message_client import MessageClient


def decode(body):
    header, trips_array = MessageClient.decode(body)
    return header, trips_array[0]


def encode_header(header):
    return MessageClient.encode_header(header)


def is_station(header):
    return header.data_type == MessageClient.STATION_DATA


def is_weather(header):
    return header.data_type == MessageClient.WEATHER_DATA


def is_eof(body):
    try:
        decode(body)
        return False
    except:
        return True



def construct_msg(header, trips_array):
    return MessageClient(
        header.data_type, header.msg_type, header.queries_suscriptions, trips_array
    ).encode()
