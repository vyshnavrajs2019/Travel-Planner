# Imports
from haversine import haversine
from user.requirements import user_requirement
from data.db import search

def controller(
		database	# Dict
	):
	# Get user requirements
	places, starts_at, ends_at, total_days, total_budget = user_requirement()

	# Search places
	lookup_fields = ['DISTRICT']
	search_results = search(database, lookup_fields, places)

	# Create matrix and mapping
	matrix, mapping = create_matrix_and_mapping(database, search_results)

	# Create route

	# If schedule fits

	# Else repeat

	pass


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
			place_b = places[i]
			point_b = (
				float(database[place_b]['COORDINATES']['LATITUDE']),
				float(database[place_b]['COORDINATES']['LONGITUDE'])
			)
			# Compute distance
			distance = haversine(point_a, point_b)
			matrix[i][j] = matrix[j][i] = distance
	return matrix, mapping