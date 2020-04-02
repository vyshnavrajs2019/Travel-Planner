import json

content = {}

with open('data/sample.json') as sample:
	content = json.loads(sample.read())

tags = set()
for place in content:
	tags.add(content[place]['TAG'])

for tag in tags:
	print(tag.upper())
	cost = float(input("COST: "))
	for place in content:
		if content[place]['TAG'] == tag:
			rating = float(content[place]['RATING'])
			content[place]['COST'] = cost * (rating/5)

with open('sample2.json', 'w') as sample:
	sample.write(json.dumps(content))