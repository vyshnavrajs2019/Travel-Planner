from setup import load_places, construct_matrix
from algo import route, sub_matrix, search
from google_map import compare_tsp_algo

places, place_names = load_places()
matrix = construct_matrix(places, place_names)

# Compare performance
compare_tsp_algo(place_names, places, matrix)