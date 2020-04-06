# Imports
from heapq import heappush, heappop
from haversine import haversine
from user.requirements import user_requirement
from data.db import search
from algorithm.path import best_route
from algorithm.scheduler import schedule

def controller(
		database	# Dict
	):
	# Get user requirements
	places, starts_at, ends_at, total_days, total_budget = user_requirement()

	# Search places
	lookup_fields = ['DISTRICT']
	search_results = search(database, lookup_fields, places)

	# Sort places according to rating
	heap = sort_places_by_rating(search_results, database)

	# Till the schedule fits
	while True:
		# Get all the remaining places
		remaining_places = []
		for rating, place in heap:
			remaining_places.append(place)

		# Create matrix and mapping
		matrix, mapping = create_matrix_and_mapping(database, remaining_places)

		# Create route
		head = best_route(matrix, len(remaining_places))

		# Get place visit order
		place_visit_order = []
		while head:
			index = head.val
			place_visit_order.append(remaining_places[index])
			head = head.next
		
		# Generate schedule
		possible, time_table = schedule(
			matrix, 			# List[List[Float]]
			mapping,			# Dict
			database,			# Dict
			place_visit_order,	# List[Str] 
			total_days,			# Int 
			starts_at,			# Int 
			ends_at,			# Int
			total_budget		# Float
		)

		# If schedule fits
		if possible:
			# Disply the schedule
			print()
			for index, each_day in enumerate(time_table):
				print('-' * 15, 'DAY', index + 1, '-' * 15)
				for each_place in each_day:
					print(each_place)
				print("\n")
			# Stop
			break

		# Else remove the place with the least rating
		heappop(heap)


def create_matrix_and_mapping(
		database,	# Dict
		places		# List[str]
	):
	# Initialize matrix and mapping
	length = len(places)
	matrix = [[0 for __ in range(length)] for _ in range(length)]
	mapping = {}
	# Construct matrix
	for i in range(length):
		# Create point A
		place_a = places[i]
		point_a = (
			float(database[place_a]['COORDINATES']['LATITUDE']),
			float(database[place_a]['COORDINATES']['LONGITUDE'])
		)
		# Create mapping
		mapping[place_a] = i
		for j in range(i + 1, length):
			# Create point B
			place_b = places[j]
			point_b = (
				float(database[place_b]['COORDINATES']['LATITUDE']),
				float(database[place_b]['COORDINATES']['LONGITUDE'])
			)
			# Compute distance
			distance = haversine(point_a, point_b)
			matrix[i][j] = matrix[j][i] = distance
	return matrix, mapping


def sort_places_by_rating(
		places,		# List[Str]
		database	# Dict
	):
	# Initialize heap
	heap = []

	# Sort places according to rating
	for place in places:
		rating = float(database[place]['RATING'])
		heappush(heap, (rating, place))

	return heap
