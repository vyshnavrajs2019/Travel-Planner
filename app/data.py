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

# Check if tag is empty
# for place in places:
# 	if places[place]['TAG'].strip() == "":
# 		print(place, places[place]['ADDRESS'])
# 		tag = input('TAG: ')
# 		places[place]['TAG'] = tag


# Check if any place name is empty	
# for place in places:
# 	if place.split(" | ")[0].strip() == "":
# 		print(place)


# Get all the keys
key_set = set()
for place, val in places.items():
	for key in val:
		key_set.add(key)
print(key_set)

save_data()


