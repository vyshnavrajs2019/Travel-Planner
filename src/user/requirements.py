def user_requirement():
	# Get the list of places
	places = ['kozhikode']# input('PLACES: ').strip().split(', ')

	# Duration
	starts_at = 6*60 #get_duration('STARTS AT')
	ends_at = 18*60 #get_duration('ENDS AT')

	# Number of days
	total_days = 5#int(input('TOTAL DAYS: '))

	# Budget
	total_budget = 20000 #int(input('TOTAL BUDGET: '))

	return places, starts_at, ends_at, total_days, total_budget
	

def get_duration(
		description # str
	):
	print(description)
	hours = int(input('HOURS: '))
	minutes = int(input('MINUTES: '))
	return hours * 60 + minutes