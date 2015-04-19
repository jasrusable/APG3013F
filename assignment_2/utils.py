import math


def to_dms(value, current_format_, delim):
    dd = ''
    if current_format_ == 'rad':
        dd = math.degrees(value)
    is_positive = dd >= 0
    dd = abs(dd)
    minutes,seconds = divmod(dd*3600,60)
    degrees,minutes = divmod(minutes,60)
    degrees = degrees if is_positive else -degrees
    return delim.join(map(str, map(int, [degrees, minutes, seconds])))

def to_radians(value, current_format_, delim):
    if current_format_ == 'dms':
        dms = value.split(delim)
        deg = float(dms[0])
        min_ = float(dms[1])
        sec = float(dms[2])
        if deg < 0:
            radians = math.radians(-(abs(deg) + (min_ / 60) + (sec / 3600)))
        else:
        	radians = math.radians(deg + (min_ / 60) + (sec / 3600))
    elif current_format_ == 'dd':
        radians =  math.radians(value)
    else:
        raise Exception('Unknown current_format_ {0}'.format(current_format_))
    return radians
