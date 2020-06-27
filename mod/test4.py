import matplotlib as mp
import csv
import numpy as np

#init
m = None
X = None
Y = None
Theta = None
def compute_cost(x,y,theta):
	h = np.dot(x,theta)	
	assert h.shape == (m, 1), "wrong shape of h,0"
	loss = 1/(2*m) * np.sum(np.power(h-Y, 2))
	return loss

def gradient_descent(x,y,theta, alpha):
	h = np.dot(x,theta)
	assert h.shape == (m, 1), "wrong shape of h,1"
	theta = theta - alpha / m * (h-y)*x 
	return theta

def main():
	global m
	with open("Book1.csv", "r") as f:
		data = [list(map(float,rec)) for rec in csv.reader(f)]
		data = np.array(data)
		m = data.shape[0]
		ones = np.full((m,1),1)
		X  = np.reshape(data[:,0],(m,1))
		X = np.append(ones,X,axis = 1)
		X = np.reshape(X, (m,2))
		print(X)
		assert X.shape == (m,2), "wrong shape without 1s"
		Y = np.reshape(data[:,1],(m,1))
		#print(X,Y)
		Theta = np.reshape(np.array([[0],[0]]),(2,1))
		print(Theta)
		alpha = 0.1
		for i in range(m):
			cost = compute_cost(X,Y, Theta)
			Theta = gradient_descent(X,Y, Theta, alpha)
		print(cost)
		print(Theta)

if __name__ == "__main__":
	main()