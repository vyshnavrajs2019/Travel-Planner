import json, time
from utils.time_format import time_format
from algo import route, create_sub_matrix, search
from google_map import test_algo, compute_cost, convert_indexes_to_places, create_driver, create_itinerary_url, GOOGLE_URL
from heapq import heappush, heappop

# Get time
def get_time(msg):
	print(msg)
	hour = int(input('Hour: '))
	mins = int(input('Minutes: '))
	return hour * 60 + mins

# Get user inputs
def get_user_inputs():
	return {
		'place': input('Place: '),
		'days': int(input('Days: ')),
		'max_places': int(input('Maximum places: ')),
		'starts_at': get_time('Starts at'),
		'ends_at': get_time('Ends at')
	}
	# return {
	# 	'place': 'kozhikode', # input('Place: '),
	# 	'days': 2, # int(input('Days: ')),
	# 	'max_places': 5, # int(input('Maximum places: ')),
	# 	'starts_at': 0, # get_time('Starts at'),
	# 	'ends_at': 0 # get_time('Ends at')
	# }

# Sort places accoring to their rating
def sort_places(search_result, places, place_names):
	heap = []
	for index in search_result:
		place = place_names[index]
		rating = float(places[place]['RATING'])
		heappush(heap, (-rating, index, place))
	return heap

def time_taken_to_visit(indexes, matrix, places, place_names):
	cost = compute_cost(indexes, matrix)
	time_taken = (cost / 25) * 60
	for index in indexes:
		place = place_names[index]
		time_taken += places[place]['TIME'] * 60
	return time_taken

# Get the best places that could be visited within the total time
def get_best_places(total_time, heap, places, place_names, matrix):
	rating, index, place = heappop(heap)
	result = [index]
	time_taken = 0
	while time_taken < total_time and len(heap):
		rating, index, place = heappop(heap)
		result.append(index)
		sub_matrix = create_sub_matrix(result, matrix)
		indexes = test_algo(result, sub_matrix)
		prev_time_taken = time_taken
		time_taken = time_taken_to_visit(indexes, matrix, places, place_names)
		if time_taken > total_time:
			result.pop()
			time_taken = prev_time_taken
	sub_matrix = create_sub_matrix(result, matrix)
	return test_algo(result, sub_matrix)
	

def generate_plan(places, place_names, matrix):
	driver = create_driver()
	driver.get(GOOGLE_URL)
	while True:
		# Get the user requirement
		user_requirement = get_user_inputs()
		# Destructure the variables
		place = user_requirement.get('place')
		days = user_requirement.get('days')
		starts_at = user_requirement.get('starts_at')
		ends_at = user_requirement.get('ends_at')
		max_places = user_requirement.get('max_places')
		# Get all places
		search_result = search(place, places)
		# Sort according to the rating
		heap = sort_places(search_result, places, place_names)
		# Collect best places
		total_time = (ends_at - starts_at) * days
		indexes = get_best_places(total_time, heap, places, place_names, matrix)
		place_order = convert_indexes_to_places(place_names, indexes, place)
		print(place_order)
		print("\n\n\n")
		url = create_itinerary_url(place_order)
		driver.get(url)