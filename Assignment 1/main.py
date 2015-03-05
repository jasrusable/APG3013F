
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from points import Point


def get_x_y_lists(list_of_points):
	x = []
	y = []
	for point in list_of_points:
		x.append(point.x)
		y.append(point.y)
	return x, y

def generate_grid_of_points(m=10,n=10):
	list_of_points = []
	for i in range(m):
		for j in range(n):
			list_of_points.append(Point(x=j, y=i))
	return list_of_points

def get_unknown_point(list_of_points):
	unknown_points = []
	for point in list_of_points:
		if point.is_unknown:
			unknown_points.append(point)
	if len(unknown_points) != 1:
		raise Exception('No unknown point in list_of_points')
	return unknown_points[0]

def generate_plot(list_of_points):
	for point in list_of_points:
		colour, marker, size = 'k', 'o', 10
		if point.is_control:
			colour, marker, size = 'k', '^', 100
		plt.scatter(point.x, point.y, s=size, c=colour, alpha=0.5, marker=marker)
	plt.show()

list_of_points = generate_grid_of_points(m=10,n=10)


list_of_points[24].is_control = True
list_of_points[24].name = 'A'
list_of_points[59].is_control = True
list_of_points[59].name = 'B'
generate_plot(list_of_points)
