def to_fixed(num, is_left=False):
	if is_left:
		return str(num).rjust(2, '0')
	else:
		return str(num)[:2].ljust(2, '0')

def time_format(curr_time, time_taken):
	# Start time
	hrs = curr_time // 60
	mins = curr_time - hrs * 60
	start_time = to_fixed(hrs, True) + ":" + to_fixed(mins)

	# End time
	hrs = (curr_time + time_taken) // 60
	mins = curr_time + time_taken - hrs * 60
	end_time = to_fixed(hrs, True) + ":" + to_fixed(mins)