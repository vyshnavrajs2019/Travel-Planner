from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from algo import route, create_sub_matrix, search
from utils.tsp import tsp
import time
from itertools import combinations, permutations

GOOGLE_URL = 'https://www.google.com/maps/dir/'
DELAY_TIME = 20

def create_driver():
	chrome_options = webdriver.ChromeOptions()
	# prefs = {"profile.managed_default_content_settings.images": 2}
	chrome_options.add_experimental_option("prefs", {})
	driver = webdriver.Chrome(chrome_options=chrome_options)
	driver.set_page_load_timeout(DELAY_TIME)
	driver.implicitly_wait(DELAY_TIME)
	return driver

def create_itinerary_url(places):
	path = "/".join(places)
	url = GOOGLE_URL + path
	return url

def get_string_repr_of_visit(array):
	return " -> ".join(map(str, array))

def compute_cost(indexes, matrix):
	cost = 0
	for i in range(1, len(indexes)):
		cost += matrix[indexes[i - 1]][indexes[i]]
	return cost

def print_order_of_visit(array):
	string = get_string_repr_of_visit(array)
	print(string)

def convert_indexes_to_places(place_names, indexes, district):
	places = []
	for index in indexes:
		name = place_names[index]
		places.append(name + " " + district)
	return places

def convert_sub_matrix_indexes_to_matrix_indexes(input_indexes, sub_matrix_indexes):
	indexes = []
	for index in sub_matrix_indexes:
		indexes.append(input_indexes[index])
	return indexes

def test_algo(input_indexes, sub_matrix):
	head = route(sub_matrix, len(sub_matrix))
	sub_matrix_indexes = []
	while head:
		index = head.val
		sub_matrix_indexes.append(index)
		head = head.next
	indexes = convert_sub_matrix_indexes_to_matrix_indexes(input_indexes, sub_matrix_indexes)
	return indexes


def test_tsp(input_indexes, sub_matrix):
	sub_matrix_indexes = tsp(sub_matrix)
	indexes = convert_sub_matrix_indexes_to_matrix_indexes(input_indexes, sub_matrix_indexes)
	return indexes


def create_itinerary(algorithm, input_indexes, sub_matrix, place_names, driver, description, district, matrix):
	print(description)
	indexes = algorithm(input_indexes, sub_matrix)
	places = convert_indexes_to_places(place_names, indexes, district)
	print_order_of_visit(places)
	# print_order_of_visit(indexes)
	print("Cost:", compute_cost(indexes, matrix))
	url = create_itinerary_url(places)
	driver.get(url)


def compare_tsp_algo(place_names, places, matrix, number_of_places=10, test_cases=14):
	driver1 = create_driver()
	time.sleep(10)
	driver2 = create_driver()
	while test_cases > 0:
		district = input('District: ')
		places_indexes = search(district, places)
		combos = combinations(places_indexes, number_of_places)
		for combo in combos:
			sub_matrix = create_sub_matrix(combo, matrix)
			create_itinerary(test_algo, combo, sub_matrix, place_names, driver1, "Zameel", district, matrix)
			create_itinerary(test_tsp, combo, sub_matrix, place_names, driver2, "TSP", district, matrix)
			time.sleep(15)
			print("\n\n\n")
		test_cases -= 1

def test_sequence(sequence, matrix, place_names):
	sub_matrix = create_sub_matrix(sequence, matrix)
	indexes = test_algo(sequence, sub_matrix)
	path = get_string_repr_of_visit(indexes)
	cost = compute_cost(indexes, matrix)
	return path, cost


def check_unique_sequence(sequence, matrix, place_names):
	perms = list(permutations(sequence))
	perm1 = perms[0]
	path, cost = test_sequence(perm1, matrix, place_names)
	outputs = [path]
	costs = [cost]
	print(outputs)
	print(costs)
	for i in range(1, len(perms)):
		perm = perms[i]
		path, cost = test_sequence(perm, matrix, place_names)
		exists = False
		for output in outputs:
			if output == path:
				exists = True
				break
		if not exists:
			outputs.append(path)
			costs.append(cost)
			print()
			print()
			print(outputs)
			print(costs)