

class Observation(object):
    def __init__(self, from_point_name=None, to_point_name=None):
        self.from_point_name = from_point_name
        self.to_point_name = to_point_name

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return "(Observation from_point:{0} to_point:{1})".format(self.from_point, self.to_point)

class DistanceObservation(Observation):
    def __init__(self, from_point_name=None, to_point_name=None, meters=None):
        Observation.__init__(self, from_point_name=from_point_name, to_point_name=to_point_name)
        self.meters = float(meters)
    def __str__(self):
        return repr(self)

    def __repr__(self):
        return ("(DistanceObservation from_point_name:{0} to_point_name:{1} meters:{2})"
            .format(self.from_point_name, self.to_point_name, self.meters))

class DirectionObservation(Observation):
    def __init__(self, from_point_name=None, to_point_name=None, radians=None):
        Observation.__init__(self, from_point_name=from_point_name, to_point_name=to_point_name)
        self.radians = float(radians)
    def __str__(self):
        return repr(self)

    def __repr__(self):
        return ("(DirectionObservation from_point_name:{0} to_point_name:{1} radians:{2})"
            .format(self.from_point_name, self.to_point_name, self.radians))

class PseudoObservation(object):
    def __init__(self, from_point=None, to_point=None, direction=None, distance=None):
        pass
