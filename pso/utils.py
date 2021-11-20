#------------------------------------------------------------------------------+
#
#	Parsa Dahesh (dinoco.parsa23@gmail.com or parsa.dahesh@studio.unibo.it)
#	Racing Line Optimization with PSO
#	MIT License, Copyright (c) 2021 Parsa Dahesh
#
#------------------------------------------------------------------------------+

import math
import matplotlib.pyplot as plt

def plot_lines(lines):
	for l in lines:
		x, y = l.xy
		plt.plot(x,y)

def get_closet_points(point, array):
	'''Closest point
	
	Given a point and an array of points, returns the array point with the lower euclidean distance to the original point.

	Parameters
	----------
	point : list
		Point coordinates
	array : list
		List of coordinates

	Returns
	-------
	result : list
		Point coordinate in the array list
	'''
	
	result = []
	distance = 1000
	for i in range(len(array)):
		temp = math.sqrt((point[0]-array[i][0])**2+(point[1]-array[i][1])**2)
		if temp<distance:
			distance = temp
			result = [array[i][0], array[i][1]]
	return result