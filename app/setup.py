import json
from haversine import haversine, Unit

# Load places
def load_places(file_name='data/sample.json'):
	places = {}
	with open(file_name) as _:
		places = json.loads(_.read())
	place_names = list(places.keys())
	# Store index in places
	for index, place in enumerate(place_names):
		places[place]['INDEX'] = index
	return places, place_names


# Construct adjacency matrix
def construct_matrix(places, place_names):
	length = len(place_names)
	matrix = [[0 for __ in range(length)] for _ in range(length)]
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
	return matrix