import math
import numpy
from file_io import get_list_of_points_from_file, get_list_of_observations_from_file
from observations import DirectionObservation


def get_distance(coordinate1, coordinate2):
    delta_y = coordinate2.y - coordinate1.y
    delta_x = coordinate2.x - coordinate1.x
    return math.sqrt((delta_y**2) + (delta_x**2))

def get_set_up_points_names(observations):
    temp = []
    for observation in observations:
        temp.append(observation.from_point_name)
    return list(reversed(['SUR12', 'SUR11', 'RU4A', 'SUR10', 'SUR09']))

def get_point_by_name(name, points):
    wanted_point = None
    for point in points:
        if name == point.name:
            wanted_point = point
    if not wanted_point:
        raise Exception('Point {0} not found.'.format(name))
    return wanted_point

def get_provisional_points(points):
    provisional_points = []
    for point in points:
        if point.type_ == 'P':
            provisional_points.append(point)
    return provisional_points

points = get_list_of_points_from_file(path='data/points.csv')

observations = get_list_of_observations_from_file(path='data/observations.csv')

set_up_point_names = get_set_up_points_names(observations)

A = numpy.matrix([
        [0,0,0,0,0,0,0,0,0,0,0],
    ])
A = numpy.delete(A, (0), axis=0)

for observation in observations:
    if isinstance(observation, DirectionObservation):
        A_row = [0,0,0,0,0,0,0,0,0,0,0]
        from_point = get_point_by_name(observation.from_point_name, points)
        to_point = get_point_by_name(observation.to_point_name, points)
        i = 0
        for unknown_point in get_provisional_points(points):
            d = get_distance(to_point, from_point)
            y = -206264.8 * (to_point.x - from_point.x) / d**2
            x = 206264.8 * (to_point.y - from_point.y) / d**2
            x = int(x)
            y = int(y)
            if to_point == unknown_point:
                A_row[i] = y
                A_row[i+1] = x
            elif from_point == unknown_point:
                A_row[i] = y
                A_row[i+1] = x
            else:
                pass
            i += 2

        j = 0
        for set_up_point_name in get_set_up_points_names(observations):
            set_up_point = get_point_by_name(set_up_point_name, points)
            if set_up_point == from_point:
                A_row[6+j] = -1
            j += 1
        A = numpy.vstack([A, A_row])

print(A)