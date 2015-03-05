
import matplotlib.pyplot as plt
from points import Point


print(Point(x=123,y=32))

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

list_of_points = generate_grid_of_points(m=10,n=10)




plt.plot(get_x_y_lists(list_of_points)[0], get_x_y_lists(list_of_points)[1], 'ro')
plt.axis([0, 20, 0, 20])
plt.show()