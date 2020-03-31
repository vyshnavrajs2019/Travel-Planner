from setup import load_places, construct_matrix
# from google_map import compare_tsp_algo, check_unique_sequence
from plan import generate_plan

places, place_names = load_places()
matrix = construct_matrix(places, place_names)

# Compare performance
# compare_tsp_algo(place_names, places, matrix)
# check_unique_sequence([54, 57, 56, 59, 68, 63, 64, 60, 55, 58], matrix, place_names)

generate_plan(places, place_names, matrix)

# Remove same places
# districts = {}
# for place in places:
# 	district = places[place]['DISTRICT']
# 	if district not in districts:
# 		districts[district] = True

# for district in districts:
# 	district_places = []
# 	for place in places:
# 		if places[place]['DISTRICT'] == district:
# 			district_places.append(place)
# 	district_places.sort()
# 	for index, place in enumerate(district_places):
# 		print(index, place)
	
# 	indexes = list(map(int, input().strip().split()))
# 	for index in indexes:
# 		place = district_places[index]
# 		del places[place]

# import json
# with open('sample2.json', 'w') as sam:
# 	sam.write(json.dumps(places))