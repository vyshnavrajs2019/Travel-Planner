from haversine import haversine, Unit

from itertools import combinations


# Generate intermediates
def intermediates(end_index, start_index, matrix_length, length):
	indices = []
	for index in range(matrix_length):
		if index != end_index and index != start_index:
			indices.append(index)
	return list(combinations(indices, length))


# Calculate shortest distance considering intermediate nodes
def shortest_distance(cache, matrix, end_index, start_index, length):
	if length == 0:
		cache[(end_index, start_index, None)] = {
			'distance': matrix[start_index][end_index], 
			'parent': start_index
		}
	else:
		intermediate_indices = intermediates(end_index, start_index, len(matrix), length)
		for combo in intermediate_indices:
			min_distance = float('inf')
			min_parent = None
			for index, last_index in enumerate(combo):
				via_indices = combo[:index] + combo[index + 1:] or None
				result = cache.get((last_index, start_index, via_indices))
				
				if min_distance > result['distance'] + matrix[last_index][end_index]:
					min_distance = result['distance'] + matrix[last_index][end_index]
					min_parent = last_index
			cache[(end_index, start_index, combo)] = {
				'distance': min_distance,
				'parent': min_parent
			}

def get_path(key, cache, start_index, path):
	path.append(key[0])
	if cache[key]['parent'] == start_index:
		path.append(start_index)
		return
	parent = cache[key]['parent']
	parent_index = key[2].index(parent)
	intermediate_indices = key[2][:parent_index] + key[2][parent_index + 1:] or None
	get_path((parent, start_index, intermediate_indices), cache, start_index, path)


# Compute tsp
def tsp(matrix, start_index=0):
	path = []
	cache = {}
	for length in range(len(matrix) - 1):
		for index in range(len(matrix)):
			if index != start_index:
				shortest_distance(cache, matrix, index, start_index, length)
	intermediate_length = len(matrix) - 2
	choice = None
	for key, val in cache.items():
		if key[2] != None and len(key[2]) == intermediate_length:
			if choice == None:
				choice = key
			elif cache[choice]['distance'] > val['distance']:
				choice = key
	get_path(choice, cache, start_index, path)
	return path

places = [
	{
		'name': 'Kallai Puzha',
		'lat': 11.2359041,
		'lng': 75.7833135,
		'time': 30
	},
	{
		'name': 'Kakkayam View Point',
		'lat': 11.5560793,
		'lng': 75.912609,
		'time': 30
	},
	{
		'name': 'Mananchira',
		'lat': 11.2544634,
		'lng': 75.7777529,
		'time': 30
	},
	{
		'name': 'Beypore Beach View',
		'lat': 11.1641618,
		'lng': 75.8023589,
		'time': 60
	},
	{
		'name': 'Kadalundi Bird Sanctuary',
		'lat': 11.1309062,
		'lng': 75.8269074,
		'time': 120
	},
	{
		'name': 'Vayalada Viewpoint',
		'lat': 11.5171451,
		'lng': 75.8593954,
		'time': 30
	}
]

def get_adjacency_matrix():
	matrix = [[float('inf') for _ in range(len(places))] for __ in range(len(places))]
	for i in range(len(places)):
		for j in range(len(places)):
			if i < j:
				matrix[i][j] = matrix[j][i] = haversine(
					(places[i]['lat'], places[i]['lng']),
					(places[j]['lat'], places[j]['lng']),
					unit=Unit.KILOMETERS
				)
	return matrix

def to_fixed(num, is_left=False):
	if is_left:
		return str(num).rjust(2, '0')
	else:
		return str(num)[:2].ljust(2, '0')

def time_format(curr_time, time_taken):
	# Start time
	hrs = curr_time // 60
	mins = curr_time - hrs * 60
	start_time = to_fixed(hrs, True) + ":" + to_fixed(mins)

	# End time
	hrs = (curr_time + time_taken) // 60
	mins = curr_time + time_taken - hrs * 60
	end_time = to_fixed(hrs, True) + ":" + to_fixed(mins)

	return [
		start_time,
		end_time
	]

def get_route(starts_at, ends_at):
	matrix = get_adjacency_matrix()
	route = tsp(matrix)
	route.reverse()
	print("\nDay 1")
	print("Duration", "\t", "Place")
	print("--------", "\t", "------------------------")
	curr_time = starts_at * 60
	prev_index = -1
	for index in route:
		if prev_index != -1:
			curr_time += round(30 * (matrix[prev_index][index]) / 5)
		start_time, end_time = time_format(curr_time, places[index]['time'])
		print(start_time + " - " + end_time, "\t", places[index]['name'])
		curr_time += places[index]['time']
		prev_index = index
	print("\n\n")

get_route(8, 22)