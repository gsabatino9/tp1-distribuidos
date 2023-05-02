import random
import string
from datetime import datetime, timedelta

def gen_data():
    # Generar datos aleatorios para la tabla Stations
    stations = []
    for i in range(200):
        code = ''.join(random.choices(string.ascii_uppercase, k=3))
        name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        latitude = round(random.uniform(-90, 90), 6)
        longitude = round(random.uniform(-180, 180), 6)
        stations.append(f"{code},{name},{latitude},{longitude},2016")
        stations.append(f"{code},{name},{latitude},{longitude},2017")

    # Generar datos aleatorios para la tabla Weather
    weathers = []
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 12, 31)
    delta = timedelta(days=1)
    while start_date <= end_date:
        date = start_date.strftime("%Y-%m-%d")
        prectot = round(random.uniform(20, 40), 2)
        qv2m = round(random.uniform(0, 20), 2)
        rh2m = round(random.uniform(0, 100), 2)
        ps = round(random.uniform(900, 1100), 2)
        t2m_range = round(random.uniform(0, 20), 2)
        ts = round(random.uniform(-30, 50), 2)
        t2mdew = round(random.uniform(-30, 50), 2)
        t2mwet = round(random.uniform(-30, 50), 2)
        t2m_max = round(random.uniform(-30, 50), 2)
        weathers.append(f"{date},{prectot},{qv2m},{rh2m},{ps},{t2m_range},{ts},{t2mdew},{t2mwet},{t2m_max}")
        start_date += delta

    # Generar datos aleatorios para la tabla Trips
    trips = []
    for i in range(100):
        start_date = random.choice(weathers).split(',')[0]
        start_station = random.choice(stations).split(',')
        end_date = (datetime.strptime(start_date, "%Y-%m-%d") + timedelta(minutes=random.randint(10, 600))).strftime("%Y-%m-%d")
        end_station = random.choice(stations).split(',')
        duration_sec = random.randint(60, 3600)
        is_member = random.choice([0, 1])
        yearid = random.choice([2016, 2017])
        trips.append(f"{start_date},{start_station[0]},{end_date},{end_station[0]},{duration_sec},{is_member},{yearid}")

    return stations, weathers, trips