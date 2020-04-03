# Imports
from data.db import load_db
import controller

# Load database
database = load_db()

# run controller
# controller.controller(database)

# Collect reviews
from chrome.reviews import (
	load_data,
	get_place,
	click_on_all_reviews,
	collect_all_reviews
)
from chrome.google_map import create_driver

START_INDEX = 0
LAST_INDEX = 0

driver = create_driver()
index = load_data()
if index == None:
	index = START_INDEX
else:
	if index > LAST_INDEX or index < START_INDEX:
		print("Your index is not between start and last!!")
		print("Please change the INDEX in your config file at chrome/config.json")
		exit()
	index = index + 1
place_names = list(database.keys())

print('CRAWLNIG STARTED\n')

for idx in range(index, LAST_INDEX + 1):
	place = place_names[idx]
	get_place(driver, place)
	if click_on_all_reviews(driver):
		collect_all_reviews(driver, place + " " + database[place]['DISTRICT'], idx)

print('\nCRAWLING FINISHED')