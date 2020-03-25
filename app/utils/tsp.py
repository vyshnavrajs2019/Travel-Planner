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