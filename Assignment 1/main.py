import math
import sympy
import numpy
import datetime
import logging
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from points import Point


logger = logging.getLogger(__name__) 
#TODO: use wraps from functools
def log_timing_decorator(task_name, logger):
    def wrap_f(f):
        def wrapped_f(*args, **kwargs):
            now = datetime.datetime.now()
            res = f(*args, **kwargs)	
            dt = datetime.datetime.now() - now
            logger.info("%s - %s" % (task_name, dt))
            return res
        return wrapped_f
    return wrap_f
    
class log_timing(object):
    def __init__(self, task_name, logger):
        self.task_name = task_name
        self.logger = logger

    def __enter__(self):
        self.now = datetime.datetime.now()

    def __exit__(self, type, value, traceback):
        dt = datetime.datetime.now() - self.now
        self.logger.error("%s - %s" % (self.task_name, dt))

class Join(object):
    def __init__ (self, from_point=None, to_point=None):
        self.from_point = from_point
        self.to_point = to_point
        distance = math.sqrt(((to_point.x - from_point.x)**2) + ((to_point.y - from_point.y)**2))
        delta_y = to_point.y - from_point.y
        delta_x = to_point.x - from_point.x
        if delta_y == 0 and delta_x > 0:
            direction = math.radians(90)
        elif delta_y == 0 and delta_x < 0:
            direction = math.radians(270)
        else:
            direction = math.atan((to_point.x - from_point.x) / (to_point.y - from_point.y))
        if to_point.y < from_point.y:
            direction += math.pi

        self.distance = distance
        self.direction = direction


class Intersection(object):
    def __init__ (self, control_point_a=None, control_point_b=None, unknown_point=None, 
        precesion_estimate_a=0.1, precesion_estimate_b=0.1):
        self.control_point_a = control_point_a
        self.control_point_b = control_point_b
        self.unknown_point = unknown_point
        self.precesion_estimate_a = precesion_estimate_a
        self.precesion_estimate_b = precesion_estimate_b

        sympy.var('an bn')
        Ax = control_point_a.x
        Ay = control_point_a.y
        Bx = control_point_b.x
        By = control_point_b.y

        Nx = (Ax + ((By - Ay) - (Bx - Ax) * sympy.tan(bn)) / (sympy.tan(an) - sympy.tan(bn)))
        Ny = Ay + (Nx - Ax) * sympy.tan(an)

        cov_X = sympy.Matrix([[0.001,0],
                            [0,0.001]])
        B = sympy.Matrix([[Nx.diff(an), Nx.diff(bn)],
                          [Ny.diff(an), Ny.diff(bn)]])
        
        cov_Y = B * cov_X * B.T

        temp_an = Join(control_point_a, unknown_point).direction
        temp_bn = Join(control_point_b, unknown_point).direction

        cov_Y =  cov_Y.subs(an, temp_an).subs(bn, temp_bn)

        self.variance_xy = cov_Y[1]
        self.variance_x = cov_Y[0] 
        self.variance_y = cov_Y[3] 

def generate_grid_of_points(m=10,n=10):
    grid_of_points = []
    
    for i in range(m):
        row = []
        for j in range(n):
            row.append(Point(x=j, y=i))
        grid_of_points.append(row)
    return grid_of_points

def generate_plot(grid_of_points):

    l = (len(grid_of_points))
    dd = 1
    y, x = numpy.mgrid[slice(0, l, dd), slice(0, l, dd)]

    z = numpy.mgrid[0:l,0:l][0]
    
    for i in range(l):
        for j in range(l):
            point = grid_of_points[i][j]
            error = 100
            if point.x_error and point.y_error:
                if math.isnan(point.x_error) or math.isnan(point.y_error):
                    error = 10.00
                else:
                    error = round(math.sqrt(point.x_error**2 + point.y_error**2), 1)
                    if error > 100:
                        error = 10
                        
            #print(error)
            z[i][j] = error

    z_min, z_max = -numpy.abs(z).max(), numpy.abs(z).max()

    plt.pcolormesh(x, y, z, cmap='RdBu')
    plt.title('pcolormesh')
    # set the limits of the plot to the limits of the data
    plt.axis([x.min(), x.max(), y.min(), y.max()])
    plt.colorbar()

    
    for row in grid_of_points:
        for point in row:
            colour, marker, size = 'k', 'o', 10
            if point.is_control:
                colour, marker, size = 'k', '^', 100
            plt.scatter(point.x, point.y, s=size, c=colour, alpha=0.5, marker=marker)

    plt.show()

def populate_error_values(grid_of_points, control_point_a, control_point_b):
    for row in grid_of_points:
        for point in row:
            if point != control_point_a and point != control_point_b:
                intersection = Intersection(
                    control_point_a=control_point_a, 
                    control_point_b=control_point_b,
                    unknown_point=point)
                point.x_error = intersection.variance_x
                point.y_error = intersection.variance_y

grid_of_points = generate_grid_of_points(m=20,n=20)

A = grid_of_points[9][9]
A.is_control = True
A.name = 'A'
B = grid_of_points[9][11]
B.is_control = True
B.name = 'B'
P = grid_of_points[2][2]

populate_error_values(grid_of_points, A, B)

generate_plot(grid_of_points)
