

class Point(object):
    name = None
    # Is control point (point with known coords)
    is_control = False
    # Is point which coords are to be determined
    is_unknown = False
    x = None
    y = None
    x_error = None
    y_error = None

    def __init__(self, name=None, is_control=None, is_unknown=None, 
        x=None, y=None, x_error=None, y_error=None):
        self.name = name
        self.is_control = is_control
        self.is_unknown = is_unknown
        self.x = x
        self.y = y
        self.x_error = x_error
        self.y_error = y_error

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return "{0}:{1}".format(self.x, self.y)