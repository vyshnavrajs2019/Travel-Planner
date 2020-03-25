import json

# Load json
def load_data():
	file_name = "save.json"
	with open(file_name) as data:
		content = data.read()
		return json.loads(content)

# Get data
places = load_data()

for place in places:
	if places[place]['TAG'].strip() == "":
		print(place)