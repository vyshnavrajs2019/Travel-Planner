# Imports
from data.db import load_db
import controller


# Load database
database = load_db()

# Maximum reviews
MAXIMUM_REVIEWS = 0
for place in database:
	MAXIMUM_REVIEWS = max(MAXIMUM_REVIEWS, int(database[place]['REVIEWS']))

# run controller
controller.controller(database, MAXIMUM_REVIEWS)