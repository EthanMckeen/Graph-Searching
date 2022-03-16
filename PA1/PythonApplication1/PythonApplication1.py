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
tree = {'S': [ ['C', 1] , ['B', 2], ['D', 10] ],
		 'B': [ ['S', 2] , ['E', 7] ],
		 'C': [ ['S', 1] , ['G', 15] ],
		 'D': [ ['S', 10] ],
		 'E': [ ['F', 1] , ['B', 7] , ['G', 2] ],
		 'F': [ ['E', 1] , ['G', 3] ],
		 'G': [ ['E', 2] , ['F', 3] , ['C', 15] ]}

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
		sum+= getCost(path[i], path[i+1], tree) #does get costCost for a node and the nextnode in the path
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
		
		


#Driver Code (ithink this is what below is called but idk im new to this)
trials = 10
#BFS
t = 0
temp = ''
bfsParent = doBFS('S', 'G', tree)
bfsPath = findPath('G', bfsParent)

t = timeit.timeit(lambda: doBFS('S', 'G', tree), number=trials)	#finds time it took to run BFS and Assign parents to explored nodes 10 times
t += timeit.timeit(lambda: findPath('G', bfsParent), number=trials)	#adds the time it takes to find the actual path from the dict of assigned parrents 10 times
t += timeit.timeit(lambda: pathCost(bfsPath, tree), number=trials) #adds time it takes to find cost of the path 10 times


print('Algorithm: BFS ')
print('\tPath Cost: ', pathCost(bfsPath, tree))
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

t = timeit.timeit(lambda: doDFS('S', 'G', tree), number=trials)	#finds time it took to run DFS and Assign parents to explored nodes 10 times
t += timeit.timeit(lambda: findPath('G', dfsParent), number=trials)	#adds the time it takes to find the actual path from the dict of assigned parrents 10 times
t += timeit.timeit(lambda: pathCost(dfsPath, tree), number=trials) #adds time it takes to find cost of the path 10 times


print('Algorithm: DFS ')
print('\tPath Cost: ', pathCost(dfsPath, tree))
#create a string detailing path
for node in dfsPath:
	temp+= node
	if node != 'G':
		temp+= ' -> '
print('\tDFS Path: ', temp)	#temp is path with pointers
print('\tExecution: ',t/trials)	#calc time for ten runs / ten to find avg run time