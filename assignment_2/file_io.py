import utils
from points import Point
from observations import DistanceObservation, DirectionObservation
from utils import to_dms


def write_file_from_list_of_points(list_of_points=None, path='output_file.csv', delim=','):
    f = open(path, 'w')
    for point in list_of_points:
        f.write(delim.join([str(point.x), str(point.y), str(point.z)]) + "\n")
    f.close()

def write_file_from_list_of_observations(list_of_observations, path='output_observations.csv', delim=','):
    with open(path, 'w') as f:
        for observation in list_of_observations:
            line_list = []
            line_list.append(str(observation.from_point_name))
            line_list.append(str(observation.to_point_name))
            if isinstance(observation, DirectionObservation):
                line_list.append(to_dms(value=observation.radians, current_format_='rad', delim='.'))
            elif isinstance(observation, DistanceObservation):
                line_list.append(str(observation.meters))
            else:
                raise Exception('Unkown observation type.')
            line_list.append('\n')
            f.write(delim.join(line_list))

def get_list_of_points_from_file(path='points.csv', delim=','):
    f = open(path, 'r')
    list_of_points = []
    for line in f.readlines():
        line = line.strip('\n')
        parts = line.split(delim)
        type_ = parts[0].strip(' ')
        name = parts[1]
        x = parts[2].strip(' ')
        y = parts[3].strip(' ')
        if type_ not in ['CP', 'P']:
            raise Exception('Points type_ is not P nor CP')
        z = 0
        list_of_points.append(
            Point(type_=type_, name=name, x=x, y=y, z=z)
        )
    return list_of_points

def get_list_of_observations_from_file(path='observations.csv', delim=','):
    f = open(path, 'r')
    list_of_observations = []
    for line in f.readlines():
        line = line.strip('\n')
        parts = line.split(delim)
        type_ = parts[0]
        from_point_name = parts[1]
        to_point_name = parts[2]
        direction = parts[3]
        distance = parts[4]
        if direction:
            radians = utils.to_radians(current_format_="dms", delim='.', value=direction)
            dir_obs = DirectionObservation(from_point_name=from_point_name,
                to_point_name=to_point_name,
                radians=radians)
            list_of_observations.append(dir_obs)
        if distance:
            meters = distance
            dist_obs = DistanceObservation(from_point_name=from_point_name,
                to_point_name=to_point_name,
                meters=meters)
            list_of_observations.append(dist_obs)
    return list_of_observations
