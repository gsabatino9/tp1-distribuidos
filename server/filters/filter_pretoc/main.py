from filter_pretoc import FilterPretoc

NAME_RECV_EXCHANGE = "filter_joined_weather_q"
NAME_RECV_QUEUE = "filter_pretoc_q"

def main():
	f = FilterPretoc(NAME_RECV_EXCHANGE, NAME_RECV_QUEUE)
	f.stop()

if __name__ == "__main__":
	main()