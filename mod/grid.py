import json
import csv
import pathfinding as gridd

		"""
		for neighbor in find_neighbors(self,(start.cx,start.cy)):
			neighbor.g = 10
			neighbor.glast = neighbor.g
			neighbor.h = Hcost(neighbor,end)
			neighbor.f = neighbor.g+neighbor.h
			parents?
			visited.append(neighbor)
			potentials.append(neighbor)
			"""
		#while visited != number of cells

				#position =  (self.gridMatrix[1,0].cy,self.gridMatrix[1,0].cx) 
		#print(position)
		#neighborlist = MGrid.find_neighbors(self,position)
		
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
def part1():
	grid_width = 19
	grid_height = 19
	grid = MGrid((grid_ưidth, grid_height))
	