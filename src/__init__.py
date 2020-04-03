# Imports
from data.db import load_db
import controller

# Load database
database = load_db()

# run controller
controller.controller(database)