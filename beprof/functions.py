import numpy as np


def subtract(curve1, curve2, def_val=0):
    """
    Function calculates difference between curve1 and curve2
    and returns new object which domain is an union
    of curve1 and curve2 domains
    Returned object is of type type(curve1)
    and has same metadata as curve1 object

    :param curve1: first curve to calculate the difference
    :param curve2: second curve to calculate the difference
    :param def_val: default value for points that cannot be interpolated
    :return: new object of type type(curve1) with element-wise difference
    (using interpolation if necessary)
    """
    coord1 = np.union1d(curve1.x, curve2.x)
    y1 = curve1.evaluate_at_x(coord1, def_val)
    y2 = curve2.evaluate_at_x(coord1, def_val)
    coord2 = y1 - y2
    # the below is explained at the end of curve.Curve.change_domain()
    obj = curve1.__class__(np.dstack((coord1, coord2))[0], **curve1.__dict__['metadata'])
    return obj


def medfilt(vector, window):
    """
    Apply a window-length median filter to a 1D array vector.

    Should get rid of 'spike' value 15.
    >>> print(medfilt(np.array([1., 15., 1., 1., 1.]), 3))
    [1. 1. 1. 1. 1.]

    The 'edge' case is a bit tricky...
    >>> print(medfilt(np.array([15., 1., 1., 1., 1.]), 3))
    [15.  1.  1.  1.  1.]

    Inspired by: https://gist.github.com/bhawkins/3535131
    """
    if not window % 2 == 1:
        raise ValueError("Median filter length must be odd.")
    if not vector.ndim == 1:
        raise ValueError("Input must be one-dimensional.")

    k = (window - 1) // 2  # window movement
    result = np.zeros((len(vector), window), dtype=vector.dtype)
    result[:, k] = vector
    for i in range(k):
        j = k - i
        result[j:, i] = vector[:-j]
        result[:j, i] = vector[0]
        result[:-j, -(i + 1)] = vector[j:]
        result[-j:, -(i + 1)] = vector[-1]

    return np.median(result, axis=1)
