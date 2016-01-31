from enum import IntEnum
import numpy as np
import scipy
from scipy.interpolate import interp1d
from scipy import signal


class Axis(IntEnum):
    """
    Axis direction (X,Y,Z). For averaged data, combination can be used, i.e. XY.
    """
    x = 1
    y = 2
    z = 3
    xy = 4


class DataSerie(np.ndarray):
    """
    1-D data serie, used in type casting for X and Y component of Curve
    """
    pass


class Curve(np.ndarray):
    """
    Curve represented by set of points on plane.
    Subclass of numpy ndarray.
    All methods which change number of points in curve (i.e. interpolate) are
    returning new objects in similar way as ndarray.
    Has additional field - info.
    """

    def __new__(cls, input_array):
        obj = np.asarray(input_array).view(cls).copy()
        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return

    @property
    def x(self):
        return self[:, 0].view(DataSerie)

    @x.setter
    def x(self, value):
        self[:, 0] = value

    @property
    def y(self):
        return self[:, 1].view(DataSerie)

    @y.setter
    def y(self, value):
        self[:, 1] = value

    def rescale(self, factor=1.0):
        self.y /= factor

    def smooth(self, window=3):
        self.y = scipy.signal.medfilt(self.y, window)

    def y_at_x(self, x):
        if x == self.x[0]:
            return x
        return np.interp(x, self.x, self.y, left=np.nan, right=np.nan)

    def __str__(self):
        ret = "shape: {}".format(self.shape) + \
              " X : [{:4.3f},{:4.3f}]".format(min(self.x), max(self.x)) + \
              " Y : [{:4.6f},{:4.6f}]".format(min(self.y), max(self.y))
        return ret

def main():
    c = Curve([[1, 0], [2, 1], [4, 0]])
    print("X:", c.x)
    print("Y:", c.y)
    for x in (0.5, 1, 1.5, 2.0, 4.5):
        print("x=", x, "y=", c.y_at_x(x))


if __name__ == '__main__':
    main()
