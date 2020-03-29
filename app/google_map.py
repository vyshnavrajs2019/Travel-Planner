from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from algo import route, create_sub_matrix, search
from utils.tsp import tsp
import time
from itertools import combinations

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

def print_order_of_visit(array):
	print(" -> ".join(map(str, array)))

def convert_indexes_to_places(place_names, indexes):
	places = []
	for index in indexes:
		name = place_names[index]
		places.append(name)
	return places


def test_algo(input_indexes, sub_matrix):
	head = route(sub_matrix, len(sub_matrix))
	indexes = []
	while head:
		index = head.val
		indexes.append(input_indexes[index])
		head = head.next
	return indexes


def test_tsp(input_indexes, sub_matrix):
	sub_matrix_indexes = tsp(sub_matrix)
	indexes = []
	for index in sub_matrix_indexes:
		indexes.append(input_indexes[index])
	return indexes


def create_itinerary(algorithm, input_indexes, sub_matrix, place_names, driver, description):
	print(description)
	indexes = algorithm(input_indexes, sub_matrix)
	places = convert_indexes_to_places(place_names, indexes)
	print_order_of_visit(places)
	print_order_of_visit(indexes)
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
			create_itinerary(test_algo, combo, sub_matrix, place_names, driver1, "Zameel")
			create_itinerary(test_tsp, combo, sub_matrix, place_names, driver2, "TSP")
			time.sleep(15)
		test_cases -= 1