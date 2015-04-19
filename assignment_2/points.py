

class Point(object):
    def __init__(self, type_=None, name=None, x=None, y=None, z=0):
        self.type_ = type_
        self.name = name
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return "(Point name: {0} x:{1} y:{2} z:{3})".format(self.name, self.x, self.y, self.z)
