from client import Client

#HOST = os.environ['HOST']
#PORT = int(os.environ['PORT'])

HOST = 'receiver'
PORT = 12345
CHUNK_SIZE = 100

def main():
	client = Client(HOST, PORT, CHUNK_SIZE)

	filepaths = ["data/montreal/", "data/toronto/", "data/washington/"]
	types_files = ["stations", "weather", "trips"]
	cities = ["montreal", "toronto", "washington"]
	client.run(filepaths, types_files, cities)
	client.stop()

if __name__ == "__main__":
	main()