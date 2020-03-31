class Node:
    def __init__(self,val,next=None):
        self.val = val
        self.next = next

def route(distance_matrix, no_of_places):
    visited_status=[]
    maximum_distance = -1
    for i in range(no_of_places):
        visited_status.append(0)
        if(sum(distance_matrix[i])>maximum_distance):
            starting_index = i
            maximum_distance=sum(distance_matrix[i])
    visited_status[starting_index]=1
    head = Node(starting_index)
    best_route=next_place(distance_matrix,visited_status,head,no_of_places,head)
    return best_route

def next_place(distance_matrix,visited_status,head,no_of_places,tail):
	#head is the starting place of route and tail is the last place
    maximum_distance=0
    # min_d=100000
    next_place_index=100000
    for i in range(no_of_places):
        distance_sum=0
        if(visited_status[i]==0):
            for j in range(no_of_places):
                if(visited_status[j]==1):
                    distance_sum+=distance_matrix[j][i]
            if(distance_sum>maximum_distance):
                maximum_distance=distance_sum
                next_place_index = i
    
    if(next_place_index==100000):
        return head
    else:
		#places the place on the suitable position 
        distance = distance_matrix[tail.val][next_place_index]
        suitable_replacement=None
        temp=head
        while(temp.next!=None):
            new_distance = distance_matrix[temp.val][next_place_index]+distance_matrix[next_place_index][temp.next.val]-distance_matrix[temp.val][temp.next.val]
            if(new_distance<distance):
                distance = new_distance
                suitable_replacement = temp
            temp=temp.next
        visited_status[next_place_index]=1
        if(suitable_replacement!=None):
            temp=suitable_replacement.next
            suitable_replacement.next=Node(next_place_index)
            suitable_replacement.next.next=temp
        else:
            tail.next=Node(next_place_index)
            tail=tail.next
        return next_place(distance_matrix,visited_status,head,no_of_places,tail)


# Construct sub matrix
def create_sub_matrix(indexes, matrix):
	indexes = list(indexes)
	length = len(indexes)
	sub_matrix = [[0 for __ in range(length)] for _ in range(length)]
	for i in range(length):
		for j in range(length):
			if i != j:
				sub_matrix[i][j] = sub_matrix[j][i] = matrix[indexes[i]][indexes[j]]
	return sub_matrix

# Search for a place
def search(query, places):
	result = set()
	query = query.lower()
	for place in places:
		if query in places[place]['DISTRICT'].lower():
			result.add(places[place]['INDEX'])
	return result