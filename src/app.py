# Imports
from data.db import load_db
from controller import controller

# Load database
database = load_db()

# run controller
controller(database)