import numpy as np 
import math
d = []

def readShrooms():
	f = open("agaricus-lepiota.txt", 'r')
	for line in f:
		d.append(line.split(','))
train_data_size = 5000
readShrooms()

accept_string = 'p'
reject_string = 'e'
"""
f = open("data.txt", 'r')
for line in f:
	d.append(line.rstrip("\n").split(','))
train_data_size = len(d)
"""
class Node(object):
	def __init__(self, d):
		self.node_list = dict()
		self.data_list = d
		self.attribute = -1
		self.prediction = False
		self.entropy = 0

Head = Node([x for x in range(0, train_data_size)])

def safe_ent(frac):
	if(frac == 0):
		return 0
	else:
		return frac*math.log(frac)
def expand(node):
	#print(node.data_list)
	#best contains how the points in this node will be partitioned
	best = dict()
	#the lowest entropy that we know of so far
	lowest_entropy = 2.0
	#the best variable to split on
	best_var = -1
	#a count of how many mushrooms were classified as poisonous
	count = 0
	for point in node.data_list:
		if(d[point][0] == accept_string):
			count+=1
	#our prediction for this node will be whichever point type, p or e, has majority
	if(2*count > len(node.data_list)):
		node.prediction = True
	#find the entropy to see if we even need to expand
	node.entropy = -1*(safe_ent(float(count)/len(node.data_list)) + safe_ent(1.0-(float(count)/len(node.data_list))))
	#if entropy is low enough then we don't need to even to expand
	if(node.entropy < 0.0001):
		return
	#iterate through all variables to find the best classification
	for var in range(1, len(d[1])):
		#next is a dictionary of how these points are partitioned by the var
		next = dict()
		#iterate through every relevant point and see its classification according to this var. Put them into next
		for point in node.data_list:
			if(d[point][var] in next):
				next[d[point][var]].append(point)
			else:
				next[d[point][var]] = [point]
		#entropy contains the expected entropy
		entropy = 0
		#calculate expected entropy
		for x in next:
			total = 0
			for point in next[x]:
				if(d[point][0] == accept_string):
					total+=1;
			entropy += len(next[x])*(safe_ent(float(total)/len(next[x])) + safe_ent(1.0-(float(total)/len(next[x]))))
		entropy /= len(node.data_list)
		entropy *= -1
		#if the entropy is the smallest, then remember it
		if(entropy < lowest_entropy):
			lowest_entropy = entropy
			best = next
			best_var = var
	#now that we've found the best, we update the node and give it children
	node.attribute = best_var
	"""
	print(lowest_entropy)
	print(best)
	print(best_var)
	"""
	#add all these nodes
	for x in best:
		child = Node(best[x])
		expand(child)
		node.node_list[x] = child
#we expand the head of the graph
expand(Head)
#DFS(Head)

total = 0
for x in range(train_data_size, len(d)):
	pos = Head
	#while it has children, or we are not at the bottom
	while(len(pos.node_list) > 0 and (d[x][pos.attribute] in pos.node_list)):
		pos = pos.node_list[d[x][pos.attribute]]
	prediction = pos.prediction
	if(prediction == (d[x][0] == 'p')):
		total+=1
print(float(total) / (len(d)-train_data_size))
