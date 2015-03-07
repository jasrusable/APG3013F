import math
import sympy
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from points import Point

MODE = 'INTERSECTION'


def join(from_, to):
	distance = math.sqrt(((to.x - from_.x)**2) + ((to.y - from_.y)**2))
	delta_y = to.y - from_.y
	delta_x = to.x - from_.x
	if delta_y == 0 and delta_x > 0:
		direction = math.radians(90)
	elif delta_y == 0 and delta_x < 0:
		direction = math.radians(270)
	else:
		direction = math.atan((to.x - from_.x) / (to.y - from_.y))
	if to.y < from_.y:
		direction += math.pi
	return distance, direction

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

Ax = sympy.Symbol('Ax')
Ay = sympy.Symbol('Ay')
By = sympy.Symbol('By')
Bx = sympy.Symbol('Bx')
an = sympy.Symbol('an')
bn = sympy.Symbol('bn')
Nx = (Ax + ((By - Ay) - (Bx - Ax) * sympy.tan(bn))/(sympy.tan(an) - sympy.tan(bn)))
Ny = Ay + (Nx - Ax) * sympy.tan(an)
print Ny.diff(bn)
Ny


A = list_of_points[0]
A.is_control = True
A.name = 'A'
B = list_of_points[1]
B.is_control = True
B.name = 'B'

print(join(A, B)[0], math.degrees(join(A, B)[1]))
#generate_plot(list_of_points)