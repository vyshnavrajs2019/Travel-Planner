from haversine import haversine, Unit


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


# Search for the place
# def 

# Get user input
def get_user_inputs():
	place = input('PLACE: ')
	days = int(input('DAYS: '))
	budget = float(input('BUDGET: '))
	starts_at = int(input('HOUR: ')) * 60 + int(input('MINUTES: '))
	ends_at = int(input('HOUR: ')) * 60 + int(input('MINUTES: '))