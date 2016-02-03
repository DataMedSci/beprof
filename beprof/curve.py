from enum import IntEnum
import numpy as np
import scipy
from scipy.interpolate import interp1d
from scipy import signal
import copy


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

    def __new__(cls, input_array, **meta):
        obj = np.asarray(input_array).view(cls)
        if meta is None:
            obj.metadata = {}
        else:
            obj.metadata = copy.deepcopy(meta)
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
              "\nX : [{:4.3f},{:4.3f}]".format(min(self.x), max(self.x)) + \
              "\nY : [{:4.6f},{:4.6f}]".format(min(self.y), max(self.y)) + \
              "\nMetadata : " + str(self.metadata)
        return ret

    # functions not ready yet, added for testing metadata purpose
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
        # Important **self.__dict__ argument
        obj = Curve([[domain[ind], y[ind]] for ind in range(0, len(y))], **self.__dict__)
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

    ###########################


def main():
    c = Curve([[1, 0], [2, 1], [4, 0]])
    print("X:", c.x)
    print("Y:", c.y)
    for x in (0.5, 1, 1.5, 2.0, 4.5):
        print("x=", x, "y=", c.y_at_x(x))

    print('\n', '*'*30, 'Metadata testing\n')

    k = Curve([[0, 1], [1, 2], [2, 3], [4, 0]], now='I', got='it')
    print('X:', k.x)
    print('Y:', k.y)
    print('M:', k.metadata)

    print(k)

    print('\nTEST:')
    test = k.fixed_step_domain(0.5, 3)
    print('X:', test.x)
    print('Y:', test.y)
    print('M:', test.metadata)

    print(test)


if __name__ == '__main__':
    main()
