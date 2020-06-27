import numpy as np
import cv2


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
		return self.start = start, self.end = end
		
		#position =  (self.gridMatrix[1,0].cy,self.gridMatrix[1,0].cx) 
		#print(position)
		#neighborlist = MGrid.find_neighbors(self,position)
		


	def AS(self, start, end):
		invalid = set()
		visited = set()
		potentials = list()

		#implement startup cells

		#while visited != number of cells
		while not visited.size == self.gridw*self.gridh:
			if start == end:
				return path
			#find the best in potentials
			for node in potentials:
				#decide the current node


			#find the neighbor with
			neighboring_nodes = find_neighbors(self,(current_node.cy,current_node.cx))

			#process the neighbors
			for neighbor in neighboring_nodes:
				if neighbor in invalid:
					continue
				if neighbor in visited and neighbor not in potentials:
					continue
				neighbor.h = Hcost(neighbor,end)
				neighbor.g = Gcost(neighbor,start)
				if neighbor.g > neighbor.glast:
					neighbor.glast = neighbor.g
				neighbor.f = neighbor.h+neighbor.g

				neighbor.parents.append(current_node)
				assert len(neighbor.parents) == 2, "Invalid parents augmentation"
				if neighbor.parents[0] > neighbor.parents[1]:
					neighbor.parents.remove[0]
				else: 
					neighbor.parents.remove[1]
				assert len(neighbor.parents) = =1, "Invalid paretns comparison"

				visited.append(neighbor)
				potentials.append(neighbor)


		
	def Gcost():
		#add gcost based off parents


	def Hcost(current_node, goal_node):
		dx = abs(current_node.cx - goal_node.x)
		dy = abs(current_node.cy - goal_node.y)
		D = 1
		return D*(dx+dy)



	def find_neighbors(self,c):
		neighbors = list()
		#c = [y,x]
		y,x = c
		possible_coord = [(y,x-1),(y+1,x), (y-1,x), (y,x+1)]
		for corner in possible_coord:
			if not corner[0] < 0 and not corner[1] < 0 and not corner[0] == self.gridh and not corner[1]==self.gridw:
				neighbors.append(self.gridMatrix[corner])	

		"""
		if not y == 0 and not x == 0:
			neighbors.add(gridMatrix[y-1,x-1])
		if not y == 0:
			neighbors.add(gridMatrix[y,x-1])
		if not y == 0 and not x == self.gridh-1:
			neighbors.add(gridMatrix[y+1,x-1])
		if not x == 0:
			neighbors.add(gridMatrix[y,x-1])
		if not x == self.gridh - 1:
			neighbors.add(gridMatrix[y,x+1])
		if not y == self.gridw - 1 and not x == 0:
			neighbors.add(gridMatrix[y+1,x+1])
		if not y == self.gridw - 1:
			neighbors.add(gridMatrix[y,x+1])
		if not y == self.gridw - 1 and not x == self.gridh - 1:
			neighbors.add(gridMatrix[y+1,x+1])
		"""
		return neighbors

grid = MGrid((5,5))
print(grid)
#def image_slicing: