import sys

INIT_DOCKER = """version: '3'
services:
  rabbitmq:
    image: rabbitmq:3-management-alpine
    container_name: rabbitmq
    ports:
      - 15672:15672
      - 5672:5672
    networks:      
      - testing_net
    healthcheck:        
      test: [ "CMD", "nc", "-z", "localhost", "5672" ]
      interval: 10s        
      timeout: 5s        
      retries: 10
    logging:
      driver: none

  receiver:
    container_name: receiver
    entrypoint: python3 /main.py
    environment:
      - PYTHONUNBUFFERED=1
      - SIZE_WORKERS={}
    image: receiver:latest
    ports:
      - 12345:12345
      - 12346:12346
    networks:      
      - testing_net
    depends_on:
      rabbitmq:
        condition: service_healthy

  <DATA_ROUTERS>

  <JOINER_STATIONS>
  <JOINER_WEATHER>

  eof_manager:
    container_name: eof_manager
    entrypoint: python3 /main.py
    environment:
      - PYTHONUNBUFFERED=1
      - SIZE_WORKERS={}
    image: eof_manager:latest
    networks:      
      - testing_net
    depends_on:
      rabbitmq:
        condition: service_healthy

networks:
  testing_net:
    driver: bridge
"""

DATA_ROUTER = """
  data_router_{}:
    container_name: data_router_{}
    entrypoint: python3 /main.py
    environment:
      - PYTHONUNBUFFERED=1
      - ID={}
    image: data_router:latest
    networks:      
      - testing_net
    depends_on:
      rabbitmq:
        condition: service_healthy
"""

JOINER_STATIONS = """
  joiner_stations:
    container_name: joiner_stations
    entrypoint: python3 /main.py
    environment:
      - PYTHONUNBUFFERED=1
    image: joiner_stations:latest
    networks:      
      - testing_net
    depends_on:
      rabbitmq:
        condition: service_healthy
"""

JOINER_WEATHER = """
  joiner_weather:
    container_name: joiner_weather
    entrypoint: python3 /main.py
    environment:
      - PYTHONUNBUFFERED=1
    image: joiner_weather:latest
    networks:      
      - testing_net
    depends_on:
      rabbitmq:
        condition: service_healthy
"""

def main():
    num_routers = int(sys.argv[1])

    routers = ""
    for i in range(1,num_routers+1):
        routers += DATA_ROUTER.format(i, i, i)

    joiner_stations = JOINER_STATIONS
    joiner_weather = JOINER_WEATHER

    compose = INIT_DOCKER.format(num_routers, num_routers) \
                  .replace("<DATA_ROUTERS>", routers) \
                  .replace("<JOINER_STATIONS>", joiner_stations) \
                  .replace("<JOINER_WEATHER>", joiner_weather)
    
    with open("docker-compose-server.yaml", "w") as compose_file:
        compose_file.write(compose)

if __name__ == "__main__":
    main()