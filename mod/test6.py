import numpy as np

class Tearable:
	m = 1
	def __init__(self):
		print(self)
		self.n = 1

m = Tearable()
m.n = 2
print(m.n)