from filter_stations_year import FilterStationsByYear
import sys, os

f = FilterStationsByYear([2016, 2017])
f.start_receiving()