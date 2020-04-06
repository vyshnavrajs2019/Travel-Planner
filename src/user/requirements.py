def user_requirement():
	# Get the list of places
	places = input('PLACES: ').strip().split(', ')

	# Duration
	starts_at = get_duration('STARTS AT')
	ends_at = get_duration('ENDS AT')

	# Number of days
	total_days = int(input('TOTAL DAYS: '))

	# Budget
	total_budget = int(input('TOTAL BUDGET: '))

	return places, starts_at, ends_at, total_days, total_budget
	

def get_duration(
		description # str
	):
	print(description)
	hours = int(input('HOURS: '))
	minutes = int(input('MINUTES: '))
	return hours * 60 + minutes