import math
import numpy
from file_io import get_list_of_points_from_file, get_list_of_observations_from_file
from observations import DirectionObservation, DistanceObservation

numpy.set_printoptions(linewidth=9000)
numpy.set_printoptions(suppress=True)
def get_distance(coordinate1, coordinate2):
    delta_y = coordinate2.y - coordinate1.y
    delta_x = coordinate2.x - coordinate1.x
    return math.sqrt((delta_y**2) + (delta_x**2))

def get_direction(coordinate1, coordinate2):
    delta_y = coordinate2.y - coordinate1.y
    delta_x = coordinate2.x - coordinate1.x
    direction = math.atan2(delta_y,delta_x)
    if delta_x < 0 and delta_y > 0:
        direction = direction 

    elif delta_x < 0 and delta_y < 0:
        direction = direction + math.pi

    elif delta_x > 0 and delta_y < 0:
        direction = direction + 2*math.pi

    return direction

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



def solve(observations):
    A = numpy.matrix([
        [0,0,0,0,0,0,0,0,0,0,0],
    ])
    A = numpy.delete(A, (0), axis=0)

    L = numpy.matrix([
            [0],
        ])
    L = numpy.delete(L, (0), axis=0)

    P = numpy.matrix([
        [0] * len(observations),
    ])
    P = numpy.delete(P, (0), axis=0)
    p = 0
    unknowns = get_provisional_points(points)
    for observation in observations:
        A_row = [0,0,0,0,0,0,0,0,0,0,0]
        P_row = [0] * len(observations)
        L_row = [0]
        from_point = get_point_by_name(observation.from_point_name, points)
        to_point = get_point_by_name(observation.to_point_name, points)
        if isinstance(observation, DirectionObservation):
            i = 0
            for unknown_point in unknowns:
                d = get_distance(to_point, from_point)
                y = 206264.806*(to_point.x - from_point.x) / d**2
                x = 206264.806*(to_point.y - from_point.y) / d**2
                if to_point == unknown_point:
                    P_row[p] = 0.01
                    A_row[i] = y
                    A_row[i+1] = -x
                elif from_point == unknown_point:
                    P_row[p] = 0.01
                    A_row[i] = -y
                    A_row[i+1] = x
                else:
                    P_row[p] = 0.25
                i += 2
            observed = observation.radians
            calculated = get_direction(from_point, to_point)
            L_row = (observed-calculated)
            print(L_row)
            j = 0
            for set_up_point_name in get_set_up_points_names(observations):
                set_up_point = get_point_by_name(set_up_point_name, points)
                if set_up_point == from_point:
                    A_row[6+j] = -1
                j += 1
        if isinstance(observation, DistanceObservation):
            P_row[p] = 4000
            i = 0
            for unknown_point in unknowns:
                distance = observation.meters
                y = (to_point.y - from_point.y) / distance
                x = (to_point.x - from_point.x) / distance
                y = round(y, 1)
                x = round(x, 1)
                if to_point == unknown_point:
                    A_row[i] = y
                    A_row[i+1] = x
                elif from_point == unknown_point:
                    A_row[i] = -y
                    A_row[i+1] = -x
                else:
                    pass
                i += 2
            observed = distance
            calculated = get_distance(to_point, from_point)
            L_row = observed - calculated
        p += 1
        L = numpy.vstack([L, L_row])
        A = numpy.vstack([A, A_row])
        P = numpy.vstack([P, P_row])
    return A, L, P

A, L, P = solve(observations)
X = (A.T * P * A).I * A.T * P * L
sigma_X = (A.T * A)**-1
V = A*X - L


