import numpy as np
import cv2
import os


class Node:
	def __init__(self, y,x):
		self.cy = y
		self.cx = x
		self.f = 0
		self.h = 0
		self.g = 0
		self.glast = 0
		self.parents = list()

class MGrid:
	def __init__(self, size):
		node = Node
		self.gridw, self.gridh = size
		self.gridMatrix = np.empty((self.gridh,self.gridw),dtype=object)
		vNode = np.vectorize(node)
		init_array_x = np.reshape(np.tile(np.arange(self.gridw),self.gridh),(self.gridh,self.gridw))
		init_array_y = init_array_x.transpose()
		self.gridMatrix[:,:] = vNode(init_array_y,init_array_x)

	def set_path(self,start,end):
		self.start = start, self.end = end


	def AS(self, start, end):
		invalid = set()
		visited = set()
		potentials = list()

		#implement startup cells
		visited.append(self.start)
		potentials.append(self.start)

		while not visited.size == self.gridw*self.gridh:
			#find the best in potentials
			smallest_h = 10000000
			for node in potentials:
				##if node in visited:
				##	continue
				if node.h < smallest_h:
					smallest_h = node.h
					current_node = node
				#decide the current node

			if current_node.cx == self.end.cx and current_node.cy == self.end.cy:
				return_list = list()
				return return_path(self.start,self.end,return_list)
			#process the neighbors
			for neighbor in find_neighbors(self,(current_node.cy,current_node.cx)):
				if neighbor in invalid:
					continue
				if neighbor in visited and neighbor not in potentials:
					continue

				neighbor.parents.append(current_node)
				if len(neighbor.parents) == 2
					if neighbor.parents[0].g > neighbor.parents[1].g:
						del neighbor.parents[0]
					else: 
						del neighbor.parents[1]
				assert len(neighbor.parents) ==1, "Invalid parents comparison"

				neighbor.h = Hcost(neighbor,self.end)
				neighbor.g = Gcost(neighbor)
				if neighbor.g > neighbor.glast:
					neighbor.glast = neighbor.g
				neighbor.f = neighbor.h+neighbor.g

				visited.append(neighbor)
				if neighbor not in potentials:
					potentials.append(neighbor)

			potentials.remove(current_node)
		print("couldn't find valid path to destination")
		os.system("pause")
		return None
		
	def Gcost(current_node):
		#add gcost based off of parents
		assert len(current_node.parents), "Multiple parents found"
		return current_node.parents[0].g + 10

	def Hcost(current_node, goal_node):
		dx = abs(current_node.cx - goal_node.x)
		dy = abs(current_node.cy - goal_node.y)
		D = 1
		return D*(dx+dy)

	def return_path(start, end, returnlist)
		if start == end:
			return returnlist.append(end.parent[0])
		return return_path(start,end.parents[0],returnlist)
		

	def find_neighbors(self,c):
		neighbors = list()
		#c = [y,x]
		y,x = c
		possible_coord = [(y,x-1),(y+1,x), (y-1,x), (y,x+1)]
		for corner in possible_coord:
			if not corner[0] < 0 and not corner[1] < 0 and not corner[0] == self.gridh and not corner[1]==self.gridw:
				neighbors.append(self.gridMatrix[corner])	
		return neighbors

grid = MGrid((5,5))
print(grid)
#def image_slicing: