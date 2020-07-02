District, starting time, ending time, total days and total budget are collected from the user. All places in the district are retrieved from the database and sorted accoring to their weighted rating.

Calculating weighted rating:
	The weighted rating for a place is calculated based on its rating, reviews and the maximum review in the database. The equation for weighted rating is 
	(1/(1+exp((-reviews*10)/MAXIMUM_REVIEWS)))*rating
	
Till the schedule for the trip fits the available time, we remove places one by one in each iteration such that the removed place will be having the least weighted rating among the places. The distance matrix is calculated and the algorithm for route generation is called by the matrix as parameter. The output of the algorithm will be a linked list containing the order in which the places are to be visited.

Calculating Distance matrix:
	The algorithm uses Haversine formula which returns the shortest distance between two geographical coordinates. The distance between two places is taken as their straight line distance.
	The output is a 2D square matrix with each element being the shortest or the straight line distance between 2 location coordinates in Kilometers.
	
	
 
