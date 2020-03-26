import json
from haversine import *

def load_file(file_name='data/sample.json'):
	with open(file_name) as data:
		content_ = json.loads(data.read())
		return content_

def load_pins(file_name='data/pincodes.json'):
	with open(file_name) as data:
		content_ = json.loads(data.read())
		return content_

def save_file(content, file_name='data/sample.json'):
	with open(file_name, 'w') as data:
		data.write(json.dumps(content))
	print('SAVED')


places = load_file()
pincodes = load_pins()
database = dict()

def remove_repeat():
	for place in places:
		name = place.strip().split("|")[0]
		name = name.strip()
		if name not in database:
			database[name] = places[place]

def remove_without_tag():
	for place in places:
		if places[place]['TAG'].strip() != "":
			database[place] = places[place]

def remove(keyword):
	for place in places:
		if keyword.lower() not in places[place]['ADDRESS'].strip().lower():
			database[place] = places[place]

def get_all_tags():
	tags = set()
	for place in places:
		tags.add(places[place]['TAG'])
	print(tags)
	print(len(tags))

def get_places_without_district_names():
	districts = ['kasargod', 'kannur', 'kozhikode', 'wayanad', 'malappuram', 'thrissur', 'palakkad', 'ernakulam', 'idukki', 'alapuzha', 'kottayam', 'pathanamthitta', 'trivandrum', 'thriuvananthapuram']
	count = 0
	for place in places:
		flag = False
		for district in districts:
			if district in places[place]['ADDRESS'].lower():
				flag = True
				break
		if not flag:
			count += 1

	print(count)

districts = {'kasaragod': [12.4156083, 75.0601568], 'kannur': [11.8666858, 75.3523103], 'kozhikode': [11.2561386, 75.6703814], 'wayanad': [11.7147961, 75.8282918], 'malappuram': [11.0619439, 76.0332862], 'palakkad': [10.7882494, 76.6188017], 'thrissur': [10.5115487, 76.1530376], 'ernakulam': [9.9711834, 76.1678608], 'idukki': [9.8564875, 76.9118412], 'alappuzha': [9.501199, 76.271893], 'pathanamthitta': [9.260413, 76.7429559], 'kollam': [8.9042253, 76.5248605], 'thiruvananthapuram': [8.5000474, 76.783734]}

def group_places():
	for place in places:
		tmp_district = None
		tmp_distance = float('inf')
		point1 = (
			float(places[place]['COORDINATES']['LATITUDE']),
			float(places[place]['COORDINATES']['LONGITUDE'])
		)
		for district in districts:
			point2 = (
				districts[district][0],
				districts[district][1]
			)
			distance = haversine(point1, point2)
			if distance < tmp_distance:
				tmp_distance = distance
				tmp_district = district
		places[place]['TMP_DISTRICT'] = tmp_district




def check_pin():
	count = 0
	for place in places:
		address = places[place]['ADDRESS']
		parts = address.split(",")
		pin = None
		for part in parts:
			ports = part.split(" ")
			for port in ports:
				if len(port) == 6:
					try:
						pin = str(int(port))
					except:
						pass
		count = 0
		dist = None
		for district in pincodes:
			if pin in pincodes[district]:
				# places[place]['DISTRICT'] = 
				count += 1
				dist = district
		
		if count == 0:
			print('NO MATCH', place)
		
		elif count > 1:
			print('MORE MAtch', place)

		else:
			places[place]['DISTRICT'] = dist[0]


	# print(count)
	# print(len(places))

load_file()
# print(len(places))
check_pin()
# remove('Karnataka')
save_file(places, 'data/sample.json')

