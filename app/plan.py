import json
from utils.time_format import time_format
from utils.tsp import tsp
from haversine import haversine, Unit
from heapq import heappop, heappush, nlargest, nsmallest

places = dict()
place_names = []
matrix = []

# districts = {'kasaragod': [12.4156083, 75.0601568], 'kannur': [11.8666858, 75.3523103], 'kozhikode': [11.2561386, 75.6703814], 'wayanad': [11.7147961, 75.8282918], 'malappuram': [11.0619439, 76.0332862], 'palakkad': [10.7882494, 76.6188017], 'thrissur': [10.5115487, 76.1530376], 'ernakulam': [9.9711834, 76.1678608], 'idukki+twp': [9.8564875, 76.9118412], 'alappuzha': [9.501199, 76.271893], 'pathanamthitta': [9.260413, 76.7429559], 'kollam': [8.9042253, 76.5248605], 'thiruvananthapuram': [8.5000474, 76.783734]}


# Load places
def load_places(file_name='data/sample.json'):
	global places, place_names
	with open(file_name) as _:
		places = json.loads(_.read())
	place_names = list(places.keys())
	# Store index in places
	for index, place in enumerate(place_names):
		places[place]['INDEX'] = index

# Construct adjacency matrix
def construct_matrix():
	global matrix
	length = len(place_names)
	matrix = [[float('inf') for __ in range(length)] for _ in range(length)]
	for i in range(length):
		point_i = (
			float(places[place_names[i]]['COORDINATES']['LATITUDE']),
			float(places[place_names[i]]['COORDINATES']['LONGITUDE'])
		)
		for j in range(i + 1, length):
			point_j = (
				float(places[place_names[j]]['COORDINATES']['LATITUDE']),
				float(places[place_names[j]]['COORDINATES']['LONGITUDE'])
			)
			distance = haversine(point_i, point_j, unit=Unit.KILOMETERS)
			matrix[i][j] = matrix[j][i] = distance


# Get time
def get_time(msg):
	print(msg)
	hour = int(input('Hour: '))
	mins = int(input('Minutes: '))
	return hour * 60 + mins


# Get places nearby
def get_nearby(index, count):
	heap = []
	length = len(place_names)
	for i in range(length):
		if i != index:
			if len(heap) < count:
				heappush(heap, (-matrix[index][i], i))
			else:
				max_distance = nlargest(1, heap)[0]
				if -max_distance[0] > matrix[index][i]:
					heappop(heap)
					heappush(heap, (-matrix[index][i], i))
	result = []
	for item in heap:
		result.append(item[1])
	return result

# Search for a place
def search(query, days, max_places):
	result = set()
	query = query.lower()
	for place in places:
		if query in places[place]['DISTRICT'].lower():
			result.add(places[place]['INDEX'])
	# indices = result.copy()
	# for index in indices:
	# 	nearby = get_nearby(index, max_places * days)
	# 	for nearby_index in nearby:
	# 		result.add(nearby_index)
	return result


# Get user inputs
def get_user_inputs():
	return {
		'place': 'kozhikode', # input('Place: '),
		'days': 2, # int(input('Days: ')),
		'max_places': 5, # int(input('Maximum places: ')),
		'starts_at': 0, # get_time('Starts at'),
		'ends_at': 0 # get_time('Ends at')
	}


# Construct sub matrix
def sub_matrix(indices):
	global matrix
	indices = list(indices)
	length = len(indices)
	mat = [[float('inf') for __ in range(length)] for _ in range(length)]
	for i in range(length):
		for j in range(length):
			if i != j:
				mat[i][j] = matrix[indices[i]][indices[j]]
	return mat


# Reduce unwanted nodes
def reduce_nodes(indices, total_time):
	heap = []
	curr_time = 0
	indices_to_remove = set()
	for index in indices:
		if curr_time < total_time:
			curr_time += places[place_names[index]]['TIME']
			heappush(heap, (places[place_names[index]]['RATING'], index))
		else:
			least_rating = nsmallest(1, heap)
			if least_rating[0] < places[place_names[index]]['RATING']:
				heappop(heap)
				curr_time -= places[place_names[least_rating[1]]]['TIME']
				indices_to_remove.add(least_rating[1])
				heappush(heap, (places[place_names[index]]['RATING'], index))
				curr_time += places[place_names[index]]['RATING']
	for index in indices_to_remove:
		indices.remove(index)
	return indices


# Get the central point
def get_central_point(indices):
	min_distance = float('inf')
	central_point = None
	for i in indices:
		max_distance = 0
		for j in indices:
			if i != j:
				max_distance = max(
					matrix[i][j],
					max_distance
				)
		if max_distance < min_distance:
			central_point = i
			min_distance = max_distance
	return central_point


# Generate plan
def generate_plan():
	user_req = get_user_inputs()
	indices = search(user_req['place'], user_req['days'], user_req['max_places'])

	# Remove unwanted
	indices = reduce_nodes(
		indices, 
		user_req['days'] * (
			user_req['ends_at'] - user_req['starts_at']
		)
	)

	mat = sub_matrix(indices)
	print('Getting your plan ready...', len(mat))
	result = tsp(mat)
	print('Your plan is ready!!\n')
	for i, index in enumerate(result):
		print(i+1, place_names[result[index]], places[place_names[result[index]]]['ADDRESS'])


# Function calls

load_places()
construct_matrix()
generate_plan()