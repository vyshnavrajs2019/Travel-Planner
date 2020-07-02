which the places are to be visited.

Calculating Distance matrix:
	The algorithm uses Haversine formula which returns the shortest distance between two geographical coordinates. The distance between two places is taken as their straight line distance.
	The output is a 2D square matrix with each element being the shortest or the straight line distance between 2 location coordinates in Kilometers.
	
	
 The distance matrix, place visited order, total days, starting time, ending time and total budget are passed as parameter to the schedule generating function. The function accepts car as the default travelling mode. To adjust the budget the algorithms assumes that if the mode of travelling is car then for each 25 Kilometers travelled a cost of 70 is deducted from the available budget. The function splits the place visit order into days by grouping all the places that could be visited on a single day. If no more places could be visited on a day because of time constraint on that day  then the place will be added to the next days schedule. If no more places could be visited because of the budget or if no more places left then the algorithm stops running thereby returning the schedule for the trip. 
 
The output of the schedule generating function will be an array with each element containing the duration, place name as the value. This output will be accepted only if the length of the array, which indicates the number of days it will take to create a trip with all these places, is less than or equal to the total days the user is going to spent else the schedule does not fit so the algorithm starts again by poping the least rated place as mentioned above.

The accepted output will be displayed to the user in the format
<DAY 1>
<Start Time - End Time> <Place Name>
<Start Time - End Time> <Place Name>
<Start Time - End Time> <Place Name>

<DAY 2>
<Start Time - End Time> <Place Name>
<Start Time - End Time> <Place Name>
<Start Time - End Time> <Place Name>
.
.
.
