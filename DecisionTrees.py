import numpy as np 
import math
d = []
def readShrooms():
	f = open("agaricus-lepiota.txt", 'r')
	for line in f:
		d.append(line.split(','))
train_data_size = 5000
readShrooms()

class Node(object):
	def __init__(self, n, d, a, p):
		self.node_list = n
		self.data_list = d
		self.attribute = a
		self.prediction = p

Head = Node([], [x for x in range(0, train_data_size)], -1, False)

def safe_log(frac):
	if(frac == 0):
		return 0
	else:
		return frac*math.log(frac)
def expand(node):
	print('hi')
	best = dict()
	lowest_entropy = 2.0
	best_var = -1
	count = 0
	for point in node.data_list:
		if(d[point][0] == 'p'):
			count+=1
	if(2*count > len(node.data_list)):
		node.prediction = True
	print(count),
	print(len(node.data_list)),
	for var in range(1, len(d[1])):
		next = dict()
		for point in node.data_list:
			if(d[point][var] in next):
				#print('hi')
				next[d[point][var]].append(point)
			else:
				next[d[point][var]] = [point]
		entropy = 0
		for x in next:
			total = 0
			for point in next[x]:
				if(d[point][0] == 'p'):
					total+=1;
			entropy += len(next[x])*(safe_log(float(total)/len(next[x])) + safe_log(1.0-(float(total)/len(next[x]))))
		entropy /= len(node.data_list)
		entropy *= -1
		if(entropy < lowest_entropy):
			lowest_entropy = entropy
			best = next
			best_var = var
	node.attribute = best_var
	print(lowest_entropy)
	if(lowest_entropy > .1):
		for x in best:
			child = Node([], best[x], -1, False)
			expand(child)
			node.node_list.append(child)

expand(Head)

total = 0
for x in range(train_data_size, len(d)):
	pos = Head
	while(len(pos.node_list) > 0):
		if(d[x][pos.attribute] in pos.node_list):
			pos = pos.node_list[d[x][pos.attribute]]
	prediction = pos.prediction
	if(prediction == (d[x][0] == 'p')):
		total+=1
print(float(total) / len(d))