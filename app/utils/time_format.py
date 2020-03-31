def to_fixed(num, digits):
	return str(num).rjust(digits, '0')

def time_format(curr_time, time_taken):
	# Start time
	hrs = curr_time // 60
	mins = curr_time - hrs * 60
	start_time = to_fixed(hrs, True) + ":" + to_fixed(mins)

	# End time
	hrs = (curr_time + time_taken) // 60
	mins = curr_time + time_taken - hrs * 60
	end_time = to_fixed(hrs, True) + ":" + to_fixed(mins)