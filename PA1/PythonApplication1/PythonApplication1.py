#						GOALS

#	Read input graph ( use Worksheet #2 P1 as an example)
#	Read the section of the algorithm to perform

#						1. BFS
#						2. DFS
#						3. UCF
#						4. A*
#	Output: Name of the algorithm tested, Path Cost, Path returned from S to G and the execution time


import timeit




#Example Graph
#P.n, h(n)-> [v,cost]

#	{S, 9}  ->	[B,2] [C,1] [D,10]
#	{B, 7}  ->	[S,2] [E,7]
#	{C, 10} ->	[S,1] [G,15]
#	{D, 7}  ->  [S,10]
#	{E, 1}  ->	[B, 7] [F,1] [G,2]
#	{F, 1}  ->	[E,1] [G,3]
#	{G, 0}  ->	[C, 15] [E,2] [F,3]

# Start at S find G


#creating graph is sorted by cost
tree = {'S': [ ['S', 0] , ['C', 1] , ['B', 2], ['D', 10] ],
		'B': [ ['B', 0] , ['S', 2] , ['E', 7] ],
		'C': [ ['C', 0] , ['S', 1] , ['G', 15] ],
		'D': [ ['D', 0] , ['S', 10] ],
		'E': [ ['E', 0] , ['F', 1] , ['B', 7] , ['G', 2] ],
		'F': [ ['F', 0] , ['E', 1] , ['G', 3] ],
		'G': [ ['G', 0] , ['E', 2] , ['F', 3] , ['C', 15] ]}

hCost = {'S': 9,
		 'B': 7,
		 'C': 10,
		 'D': 7,
		 'E': 1,
		 'F': 1,
		 'G': 0}



#used Functions
def getEdges(k, tree):
	edges= []

	for i in tree.get(k):
		edges.append(i[0])

	return edges # a list of strings with edge title


def getCost(k, v, tree):
	b = True
	temp= []
	temp = tree.get(k)

	for i in temp:
		if i[0] == v:
			return i[1];	# a int of the cost
		else:
			b = False
	if b == False:
		return math.inf	   #infinity meaning there is no edge 


def findPath(goal, parent):
	path = [goal]
	node = goal
	while path[0] != 'null':
		node=parent.get(node)
		path.insert(0, node) #sticks the parent behind the node
	path.pop(0)	#removes 'null'
	return path			#a list of the path where path[0] is source and path[-1] is goal


def pathCost(path, tree):
	sum=0;
	for i in range(0, len(path)-1):
		sum+= getCost(path[i], path[i+1], tree) #does recursively get costCost for a node and the nextnode in the path
	return sum	# int total cost of a given path


#THE ALGORITHMS
def doBFS(start, goal, tree):
	explored = ['null']
	fQueue = [start]
	found = []
	parent = { start : 'null'}

	while explored[-1] != goal:
		#print(fQueue) #to see if the fqueue is correct
		explored.append(fQueue[0]) #grabs first item in queue and puts it into explored to be explored
		fQueue.pop(0)			   #removes first item in queue
		if explored[-1] == goal:
			break				#stops if goal is found

		found = getEdges(explored[-1], tree) #finds edges of the node being explored

		for node in found:	#sets the explored node as the parent for each found node
			if node not in explored: #checks hey have i been explored
				if node not in parent.keys(): #checks hey do i have a parent
					parent[node] = explored[-1]	#sets parent
					fQueue.append(node)			#adds node to frontier queue
	return parent #returns a dict to find path 


def doDFS(start, goal, tree):
	explored = ['null']
	fStack = [start] #we are going right to left of this list filo
	found = []
	parent = { start : 'null'}

	while explored[-1] != goal:
		#print(fStack) #to see if the fStack is correct
		explored.append(fStack[-1])#grabs top item in stack and puts it into explored to be explored
		fStack.pop(-1) #removes top item from stack
		if explored[-1] == goal:
			break				#stops if goal is found

		found = getEdges(explored[-1], tree) #finds edges of the node being explored
		found.reverse() #this makes it so the least costing path is now right most towards the top of the stack

		for node in found:
			if node not in explored:
				parent[node] = explored[-1]
				fStack.append(node)
	return parent
		
		
def doUCF(start, goal, tree):
	explored = ['null']
	fPriorityQ = [start] 
	found = []
	parent = { start : 'null'}
	uCost = { 'S' : 0}
	temp = 0

	while explored[-1] != goal:
		#print(fPriorityQ) #to see if the fPriorityQ is correct
		explored.append(fPriorityQ[0]) #grabs first item in queue and puts it into explored to be explored
		fPriorityQ.pop(0)			   #removes first item in queue
		if explored[-1] == goal:
			break				#stops if goal is found

		found = getEdges(explored[-1], tree) #finds edges of the node being explored

		for node in found:	
			if node not in explored: #checks hey have i been explored
				if node in uCost: #do i have an existing cost
					temp = uCost.get(explored[-1]) + getCost(explored[-1], node, tree) #calc this pathing cost
					if temp < uCost.get(node): # if new < old update parent and cost
						parent.update({node: explored[-1]}) #updates parent if cheaper
						uCost.update({node: temp}) #update cost
				else:
					parent[node] = explored[-1] #sets parent of node
					uCost[node] = uCost.get(parent.get(node)) + getCost(parent.get(node), node, tree)
					fPriorityQ.append(node)		#adds node to frontier Priority Q

		fPriorityQ.sort(key=uCost.get) #sort Priorityq by uCost meaning fPriorityQ[0]<fPriorityQ[1]<fPriorityQ[2]

		
	return [parent, uCost.get(goal)]  #returns a dict to find path 


def doAstar(start, goal, tree, hCost):
	explored = ['null']
	fPriorityQ = [start] 
	found = []
	parent = { start : 'null'}
	uCost = { 'S' : 0}
	aCost={'S': uCost.get('S') + hCost.get('S')} # f(p)= c(p) + h(p)
	temp = 0

	while explored[-1] != goal:
		#print(fPriorityQ) #to see if the fPriorityQ is correct
		explored.append(fPriorityQ[0]) #grabs first item in queue and puts it into explored to be explored
		fPriorityQ.pop(0)			   #removes first item in queue
		if explored[-1] == goal:
			break				#stops if goal is found

		found = getEdges(explored[-1], tree) #finds edges of the node being explored

		for node in found:	
			if node not in explored: #checks hey have i been explored
				if node in uCost: #do i have an existing cost
					temp = uCost.get(explored[-1]) + getCost(explored[-1], node, tree) #calc the current pathing cost
					if temp < uCost.get(node): # if current < existing cost update parent and cost
						parent.update({node: explored[-1]}) #updates parent if cheaper
						uCost.update({node: temp}) #update cost
				else:
					parent[node] = explored[-1] #sets parent of node
					uCost[node] = uCost.get(parent.get(node)) + getCost(parent.get(node), node, tree) #set uCost
					fPriorityQ.append(node)		#adds node to frontier Priority Q
				aCost[node]= uCost.get(node) + hCost.get(node)

		fPriorityQ.sort(key=aCost.get) #sort Priorityq by aCost meaning fPriorityQ[0]<fPriorityQ[1]<fPriorityQ[2] etc etc

		
	return [parent, uCost.get(goal)]  #returns a dict to find path 













#Driver Code (ithink this is what below is called but idk im new to this)
trials = 10
#BFS
t = 0
temp = ''
bfsParent = doBFS('S', 'G', tree)
bfsPath = findPath('G', bfsParent)
bfsCost = pathCost(bfsPath, tree)

t = timeit.timeit(lambda: doBFS('S', 'G', tree), number=trials)	#finds time it took to run BFS and Assign parents to explored nodes 10 times
t += timeit.timeit(lambda: findPath('G', bfsParent), number=trials)	#adds the time it takes to find the actual path from the dict of assigned parrents 10 times
t += timeit.timeit(lambda: pathCost(bfsPath, tree), number=trials) #adds time it takes to find cost of the path 10 times


print('Algorithm: BFS ')
print('\tPath Cost: ', bfsCost)
#create a string detailing path
for node in bfsPath:
	temp+= node
	if node != 'G':
		temp+= ' -> '
print('\tBFS Path: ', temp)	#temp is path with pointers
print('\tExecution: ',t/trials)	#calc time for ten runs / ten to find avg run time

#DFS
t = 0
temp = ''
dfsParent = doDFS('S', 'G', tree)
dfsPath = findPath('G', dfsParent)
dfsCost = pathCost(dfsPath, tree)

t = timeit.timeit(lambda: doDFS('S', 'G', tree), number=trials)	#finds time it took to run DFS and Assign parents to explored nodes 10 times
t += timeit.timeit(lambda: findPath('G', dfsParent), number=trials)	#adds the time it takes to find the actual path from the dict of assigned parrents 10 times
t += timeit.timeit(lambda: pathCost(dfsPath, tree), number=trials) #adds time it takes to find cost of the path 10 times


print('Algorithm: DFS ')
print('\tPath Cost: ', dfsCost)
#create a string detailing path
for node in dfsPath:
	temp+= node
	if node != 'G':
		temp+= ' -> '
print('\tDFS Path: ', temp)	#temp is path with pointers
print('\tExecution: ',t/trials)	#calc time for ten runs / ten to find avg run time

#UCF
t = 0
temp = ''
ucfInfo = doUCF('S', 'G', tree)
ucfParent = ucfInfo[0]
ucfCost = ucfInfo[1]
ucfPath = findPath('G', ucfParent)

t = timeit.timeit(lambda: doUCF('S', 'G', tree), number=trials) #finds time it took to run UCF and assign parents and find unified costs 10 times
t += timeit.timeit(lambda: findPath('G', ucfParent), number=trials) #adds time it takes to find path from parent 10 times

print('Algorithm: UCF ')
print('\tPath Cost: ', ucfCost)
#create a string detailing path
for node in ucfPath:
	temp+= node
	if node != 'G':
		temp+= ' -> '
print('\tUCF Path: ', temp)	#temp is path with pointers
print('\tExecution: ',t/trials)	#calc time for ten runs / ten to find avg run time

#A*
t = 0
temp = ''
astarInfo= doAstar('S', 'G', tree, hCost)
astarParent = astarInfo[0]
astarCost= astarInfo[1]
astarPath = findPath('G', astarParent)

t = timeit.timeit(lambda: doAstar('S', 'G', tree, hCost), number=trials) #finds time it took to run Astar and assign parents and find unified costs 10 times
t += timeit.timeit(lambda: findPath('G', astarParent), number=trials) #adds time it takes to find path from parent 10 times

print('Algorithm: A* ')
print('\tPath Cost: ', astarCost)
#create a string detailing path
for node in astarPath:
	temp+= node
	if node != 'G':
		temp+= ' -> '
print('\tA* Path: ', temp)	#temp is path with pointers
print('\tExecution: ',t/trials)	#calc time for ten runs / ten to find avg run time