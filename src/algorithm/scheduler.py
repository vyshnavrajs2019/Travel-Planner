# Imports
from datetime import datetime, timedelta
from utils import time_format


def schedule(
		matrix, 			# List[List[Float]]
		mapping,			# Dict
		database,			# Dict
		place_visit_order,	# List[Str] 
		days,				# Int 
		starts_at,			# Int 
		ends_at				# Int
	):
	# Split into days
	time_table = split_to_days(matrix, mapping, database, place_visit_order, starts_at, ends_at)
	# Check if schedule fits
	if len(time_table) <= days:
		return True, time_table
	# If not able to fit then notify caller
	return False, time_table


def split_to_days(
		matrix, 			# List[List[Float]]
		mapping,			# Dict
		database,			# Dict
		place_visit_order,	# List[Str]
		starts_at,			# Int 
		ends_at				# Int
	):
	# Initialize the time table to store the schedule
	time_table = []
	# Create current datetime for start time
	current_datetime = get_datetime(datetime.today(), starts_at)
	# Create current datetime for end time
	current_end_datetime = get_datetime(datetime.today(), ends_at)
	# For all places combine travel time and time spent at the place
	another_day = True
	for index, place in enumerate(place_visit_order):
		# If another day add a list to time table to store next days schedule
		if another_day:
			time_table.append([])
		# Add schedule to time table
		schedule_repr = get_string_repr_duration_and_place(current_datetime, place, database[place]['TIME'])
		time_table[-1].append(schedule_repr)
		# Get datetime after spent
		current_datetime = get_datetime_after_spent(current_datetime, database[place]['TIME'])
		# Check if no more places are to be visited
		if index + 1 >= len(place_visit_order):
			continue
		# Check if next place can be reached
		if not can_next_place_be_reached(mapping, matrix, index, place_visit_order, current_datetime, current_end_datetime):
			# Set flag and compute remaining time delta
			another_day = True
			next_place_reach_datetime = get_next_place_reach_datetime(mapping, matrix, index, place_visit_order, current_datetime)
			remaining_timedelta = next_place_reach_datetime - current_end_datetime
			# Get next days current datetime and add remaining time delta
			current_datetime = get_datetime(current_datetime,starts_at)
			current_datetime = current_datetime + remaining_timedelta
			continue
		# Check if next place can be visited
		current_datetime = get_next_place_reach_datetime(mapping, matrix, index, place_visit_order, current_datetime)
		# Check if next place can be visited
		if not can_next_place_be_visited(database, index, place_visit_order, current_datetime, current_end_datetime):
			another_day = True
			current_datetime = get_datetime(current_datetime, starts_at)
	return time_table


def get_datetime(
		current_datetime,	# DateTime
		minutes				# Int
	):
	# Create a time delta
	next_day = timedelta(days=1)
	# Set hour and minutes
	hour = int(minutes // 60)
	minute = int(minutes - hour * 60)
	# Initialize new datetime
	new_datetime = datetime(current_datetime.year, current_datetime.month, current_datetime.day, hour, minute)
	# Set new datetime to next day
	new_datetime = new_datetime + next_day
	return new_datetime


def get_string_repr_duration_and_place(
		current_datetime,			# DateTime
		place,						# Str
		spent_time					# Float
	):
	# DateTime after spent
	end_datetime = get_datetime_after_spent(current_datetime, spent_time)
	# Get time format of start and end time
	start_time_format = time_format(current_datetime.hour, current_datetime.minute)
	end_time_format = time_format(end_datetime.hour, end_datetime.minute)
	return f'{ start_time_format } - { end_time_format } - { place }'


def get_datetime_after_spent(
		current_datetime,	# DateTime
		spent_time			# Int
	):
	# Initialize timedelta for spent time
	spent_duration_timedelta = timedelta(hours=spent_time)
	# Initialize end datetime
	end_datetime = current_datetime + spent_duration_timedelta
	return end_datetime


def convert_distance_to_time(
		distance,	# Float
		mode='CAR'	# Str
	):
	# Initialize traveling modes
	MODES = { 'CAR': 25 }
	# Get time taken
	time_taken = distance // MODES[mode]
	return time_taken


def can_next_place_be_reached(
		mapping,				# Dict
		matrix,					# List[List[Int]]
		current_index,			# Int
		place_visit_order,		# List[Str]
		current_datetime,		# DateTime	
		current_end_datetime,	# DateTime
	):
	next_place_reach_datetime = get_next_place_reach_datetime(mapping, matrix, current_index, place_visit_order, current_datetime)
	if next_place_reach_datetime > current_end_datetime:
		return False
	return True


def get_next_place_reach_datetime(
		mapping,			# Dict
		matrix,				# List[List[Int]]
		current_index,		# Int
		place_visit_order,	# List[Str]
		current_datetime	# DateTime
	):
	# Compute time taken to reach next place
	time_taken_to_reach_next_place = get_time_taken_to_reach_next_place(mapping, matrix, current_index, place_visit_order)
	time_delta_to_reach_next_place = timedelta(hours=time_taken_to_reach_next_place)
	next_place_reach_datetime = current_datetime + time_delta_to_reach_next_place
	return next_place_reach_datetime


def get_time_taken_to_reach_next_place(
		mapping,			# Dict
		matrix,				# List[List[Int]]
		current_index,		# Int
		place_visit_order	# List[Str],
	):
	# Get current place
	current_place = place_visit_order[current_index]
	# Get next place and its index
	next_place_index = current_index + 1
	next_place = place_visit_order[next_place_index]
	# Get the mapping index of current and next places
	map_index_current_place = mapping[current_place]
	map_index_next_place = mapping[next_place]
	# Compute the distance
	distance = matrix[map_index_current_place][map_index_next_place]
	# Convert distance to time
	time_taken = convert_distance_to_time(distance)
	return time_taken


def can_next_place_be_visited(
		database,				# Dict
		current_index,			# Int
		place_visit_order,		# List[Str]
		current_datetime,		# DateTime	
		current_end_datetime,	# DateTime
	):
	# Get next place index, next place and visit time
	next_index = current_index + 1
	next_place = place_visit_order[next_index]
	spend_time = database[next_place]['TIME']
	# Get datetime after visit
	after_visit_datetime = get_datetime_after_spent(current_datetime, spend_time)
	# Check if datetime <= end datetime
	if after_visit_datetime <= current_end_datetime:
		return True
	return False