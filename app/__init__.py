from setup import load_places, construct_matrix
from algo import route, create_sub_matrix, search
from google_map import compare_tsp_algo, check_unique_sequence

places, place_names = load_places()
matrix = construct_matrix(places, place_names)

# Compare performance
compare_tsp_algo(place_names, places, matrix)
# check_unique_sequence([54, 57, 56, 59, 68, 63, 64, 60, 55, 58], matrix, place_names)