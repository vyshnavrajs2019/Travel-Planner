from selenium import webdriver
from selenium.webdriver.common.keys import Keys

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

def compare_tsp_algo():
	algo_driver = create_driver()
	tsp_driver = create_driver()
	t = 14
	while t > 0:
		district = input('District: ')
		indexes = search(district)
		combos = combinations(indexes, 10)
		for combo in combos:
			mat = sub_matrix(combo)
			# Zams algo
			head = route(mat.copy(), len(combo))
			indices1 = []
			start_index = None
			while head:
				if start_index == None:
					start_index = head.val
				indices1.append(combo[head.val])
				head = head.next
			places1 = []
			for index in indices1:
				places1.append(place_names[index])
			print("\n\n")
			print("ZAMEEL")
			print(" -> ".join(places1))
			print(" -> ".join(map(str, indices1)))
			param1 = "/".join(places1)
			driver1.get(GOOGLE_URL + param1)
			# TSP

			indices2 = tsp(mat.copy(), start_index)
			places2 = []
			idx = []
			for index in indices2:
				idx.append(combo[index])
				places2.append(place_names[combo[index]])
			print("\n")
			print("TSP")
			print(" -> ".join(places2))
			print(" -> ".join(map(str, idx)))
			param2 = "/".join(places2)
			driver2.get(GOOGLE_URL + param2)
			time.sleep(30)

		t -= 1
	