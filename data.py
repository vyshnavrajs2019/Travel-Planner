import json

# Load json
def load_data():
	file_name = "save.json"
	with open(file_name) as data:
		content = data.read()
		return json.loads(content)

# Save data
def save_data():
	file_name = "save.json"
	with open(file_name, "w") as data:
		data.write(json.dumps(places))

# Get data
places = load_data()

for place in places:
	if places[place]['TAG'].strip() == "":
		print(place, places[place]['ADDRESS'])
		tag = input('TAG: ')
		places[place]['TAG'] = tag
	


save_data()


