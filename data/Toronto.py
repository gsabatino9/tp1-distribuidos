import csv
from gen_data.gen_data import gen_data
stations, weathers, trips = gen_data()

with open('Toronto/stations.csv', mode='w', newline='\n') as file:
    writer = csv.writer(file)
    for station in stations:
        writer.writerow(station.split(','))        

with open('Toronto/weather.csv', mode='w', newline='\n') as file:
    writer = csv.writer(file)
    for station in weathers:
        writer.writerow(station.split(','))

with open('Toronto/trips.csv', mode='w', newline='\n') as file:
    writer = csv.writer(file)
    for station in trips:
        writer.writerow(station.split(','))