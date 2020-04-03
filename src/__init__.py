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
LAST_INDEX = 10

driver = create_driver()
START_INDEX = load_data()
if START_INDEX == None:
	START_INDEX = 0
else:
	START_INDEX = START_INDEX + 1
place_names = list(database.keys())

for idx in range(START_INDEX, LAST_INDEX + 1):
	place = place_names[idx]
	get_place(driver, place)
	if click_on_all_reviews(driver):
		collect_all_reviews(driver, place + " " + database[place]['DISTRICT'], idx)
	