import numpy as np

def subtract(curve1, curve2, defval=0):
    '''
    Function calculates difference between curve1 and curve2 and returns new object
    which domain is an union of domains of curve1 and curve2
    Returned object is of type type(curve1) and has same metadata as curve1 object

    :param curve1: first curve to calculate the difference
    :param curve2: second curve to calculate the difference
    :param defval: default value for points that cannot be interpolated
    :return: new object of type type(curve1) with element-wise difference (using interpolation if necessary)
    '''
    coord1 = np.union1d(curve1.x, curve2.x)
    y1 = curve1.evaluate_at_x(coord1, defval)
    y2 = curve2.evaluate_at_x(coord1, defval)
    coord2 = y1 - y2
    obj = curve1.__class__(np.stack((coord1, coord2), axis=1), **curve1.__dict__['metadata'])
    return obj
