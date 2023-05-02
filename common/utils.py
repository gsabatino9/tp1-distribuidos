import os
import logging

from configparser import ConfigParser


def initialize_log():
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level='INFO',
        datefmt='%Y-%m-%d %H:%M:%S',
    )


def initialize_config(params=[]):
    config = ConfigParser(os.environ)
    config_params = {}
    try:
        for value in params:
            config_params[value] = config["DEFAULT"][value]
    except KeyError as e:
        raise KeyError("Key was not found. Error: {} .Aborting server".format(e))
    except ValueError as e:
        raise ValueError("Key could not be parsed. Error: {}. Aborting server".format(e))
    return config_params

def decode(msg):
	return msg.decode('utf-8')

def split_city(msg, splitted=False):
	if not splitted:
		msg = msg.split(',')

	city = msg[0]
	data = msg[1:]

	return city, data