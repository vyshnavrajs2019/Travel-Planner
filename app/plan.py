import json, time
from utils.time_format import time_format


# Get time
def get_time(msg):
	print(msg)
	hour = int(input('Hour: '))
	mins = int(input('Minutes: '))
	return hour * 60 + mins

# Get user inputs
def get_user_inputs():
	return {
		'place': 'kozhikode', # input('Place: '),
		'days': 2, # int(input('Days: ')),
		'max_places': 5, # int(input('Maximum places: ')),
		'starts_at': 0, # get_time('Starts at'),
		'ends_at': 0 # get_time('Ends at')
	}