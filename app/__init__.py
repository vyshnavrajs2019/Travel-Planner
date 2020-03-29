from setup import load_places, construct_matrix
from algo import route, sub_matrix, search

places, place_names = load_places()
matrix = construct_matrix(places, place_names)

