import json, time
from utils.time_format import time_format, to_fixed
from algo import route, create_sub_matrix, search
from google_map import test_algo, compute_cost, convert_indexes_to_places, create_driver, create_itinerary_url, GOOGLE_URL, convert_indexes_to_places_without_district
from heapq import heappush, heappop
from datetime import datetime, timedelta

# Convert to hour and minutes
def convert_to_string_repr_time(minutes):
	hours = int(minutes//60)
	mins = int(minutes - hours*60)
	return f'{to_fixed(hours, 2)} hr {to_fixed(mins, 2)} mins'

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
		# 'max_places': int(input('Maximum places: ')),
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
	return time_taken, (cost/25) * 60

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
		time_taken, travel_time = time_taken_to_visit(indexes, matrix, places, place_names)
		if time_taken > total_time:
			result.pop()
			time_taken = prev_time_taken
	sub_matrix = create_sub_matrix(result, matrix)
	indexes = test_algo(result, sub_matrix)
	time_taken, travel_time = time_taken_to_visit(indexes, matrix, places, place_names)
	print('Total Time :', convert_to_string_repr_time(total_time))
	print('Remaining Time:', convert_to_string_repr_time(total_time - time_taken))
	print('Travel Time:', convert_to_string_repr_time(travel_time))
	return indexes

def get_date_time(time_, curr_datetime=datetime.today()):
	tomorrow = curr_datetime + timedelta(days=1)
	year = tomorrow.year
	month = tomorrow.month
	day = tomorrow.day
	curr = datetime(year, month, day, int(time_//60), int(time_ - int(time_//60)*60))
	return curr

def make_schedule(matrix, starts_at, ends_at, days, place_order, places):
	curr = get_date_time(starts_at)
	end  = get_date_time(ends_at)
	day_num = 1
	print('\n\n')
	print('-'*20 + 'Day ' + str(day_num) + '-'*20)
	for index, place in enumerate(place_order):
		hour = curr.hour
		mins = curr.minute
		after_spent = curr + timedelta(minutes=int(places[place]['TIME'] * 60))
		print(f'{to_fixed(hour, 2)}:{to_fixed(mins, 2)} - {to_fixed(after_spent.hour, 2)}:{to_fixed(after_spent.minute, 2)} -', place)
		if index + 1 < len(place_order):
			# More places
			curr_index = places[place]['INDEX']
			next_index = places[place_order[index + 1]]['INDEX']
			km = matrix[curr_index][next_index]
			time_taken = int(places[place]['TIME'] * 60 + (km/25)*60 + places[place_order[index + 1]]['TIME'] * 60)
			delta = timedelta(minutes=time_taken)
			if curr + delta <= end:
				curr = curr + delta - timedelta(minutes=int(places[place_order[index + 1]]['TIME'] * 60))
			else:
				print()
				day_num += 1
				print('-'*20 + 'Day ' + str(day_num) + '-'*20)
				prev= curr
				curr = get_date_time(starts_at, curr)
				curr += timedelta(minutes=int((km/25)*60))
				end  = get_date_time(ends_at, prev)


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
		# max_places = user_requirement.get('max_places')
		# Get all places
		search_result = search(place, places)
		# Sort according to the rating
		heap = sort_places(search_result, places, place_names)
		# Collect best places
		total_time = (ends_at - starts_at) * days
		indexes = get_best_places(total_time, heap, places, place_names, matrix)
		place_order = convert_indexes_to_places(place_names, indexes, place)
		place_order_2 = convert_indexes_to_places_without_district(place_names, indexes)
		make_schedule(matrix, starts_at, ends_at, days, place_order_2, places)
		print("\n\n\n")
		print(place_order)
		url = create_itinerary_url(place_order)
		driver.get(url)