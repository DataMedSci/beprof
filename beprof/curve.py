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

    def change_domain(self, domain):

        # check if new domain includes in the orginal domain
        if np.max(domain) > np.max(self.x):
            # maybe some exception here or stderr log ?
            # these prints only for testing purpose
            print('Error1')
            print('domain.max: ', np.max(domain), '|| self.max: ', np.max(self.x))
            return self
        if np.min(domain) < np.min(self.x):
            print('Error2')
            print('domain.min: ', np.min(domain), '|| self.min: ', np.min(self.x))
            return self
        y = np.interp(domain, self.x, self.y)
        obj = Curve([[domain[ind], y[ind]] for ind in range(0, len(y))])
        return obj

    def fixed_step_domain(self, step=0.1, fixp=0):
        section = (np.min(self.x), np.max(self.x))
        if fixp < section[0] or fixp > section[1]:
            # some kind of error just as in change_domain above?
            print("Section: ", section, "fixp: ", fixp)
            print('Error3')
            return self
        count = int(np.min([fixp - section[0], section[1] - fixp]) / step)
        domain = [fixp + n * step for n in range(-count, count+1)]
        return self.change_domain(domain)

    def __str__(self):
        ret = "shape: {}".format(self.shape) + \
              " X : [{:4.3f},{:4.3f}]".format(min(self.x), max(self.x)) + \
              " Y : [{:4.6f},{:4.6f}]".format(min(self.y), max(self.y))
        return ret


def main():
    c = Curve([[0, 0], [5, 5], [10, 0]])
    print("X:", c.x)
    print("Y:", c.y)
    for x in (0.5, 1, 1.5, 2.0, 4.5):
        print("x=", x, "y=", c.y_at_x(x))


    print('\n', '*'*30,'\nchange_domain:')

    print("X:", c.x)
    print("Y:", c.y)
    new = c.change_domain([1, 2, 3, 5, 6, 7, 9])
    print("X:", new.x)
    print("Y:", new.y)

    print('\n', '*'*30,'\nfixed_step_domain:')

    print("X:", c.x)
    print("Y:", c.y)
    test = c.fixed_step_domain(0.4, 7)
    print("X:", test.x)
    print("Y:", test.y)

if __name__ == '__main__':
    main()
