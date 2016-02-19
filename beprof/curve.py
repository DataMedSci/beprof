from enum import IntEnum
import numpy as np
import scipy
from scipy.interpolate import interp1d
from scipy import signal
import math
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

    Extra metadata can be added to Curve object and is stored in a dictionary.
    This data can be basically anything: date of measurement, string describing
    gathered data, extra informations etc.

    One can add metadata to Curve object in 2 ways:
        1) When creating object, using extra arguments (**kwargs)
        2) When object (obj) alrady exists, one can use dictionary methods
           to add a field to obj.metadata dict.

    """

    def __new__(cls, input_array, **meta):
        obj = np.asarray(input_array).view(cls)
        if meta is None:
            obj.metadata = {}
        else:
            obj.metadata = copy.deepcopy(meta)
        return obj

    def __array_finalize__(self, obj):
        if obj is None: # what generally means the object was created using explicit constructor
            return
        self.metadata = getattr(obj, 'metadata', {})

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
        '''
        Creating new Curve object in memory with domain passed as a parameter.
        New domain must include in the orignal domain.
        Copies values from orginal curve and uses interpolation to calculate
        values for new points in domain.

        Calculate y - values of example curve with changed domain:
        >>> print(Curve([[0,0], [5, 5], [10, 0]]).change_domain([1, 2, 8, 9]).y)
        [ 1.  2.  2.  1.]

        :param domain: set of points representing new domain. Might be a list or np.array
        :return: new Curve object with domain set by 'domain' parameter
        '''

        # check if new domain includes in the orginal domain
        if np.max(domain) > np.max(self.x):
            # separate issue created to provide logging package
            print('Error1')
            return self
        if np.min(domain) < np.min(self.x):
            print('Error2')
            return self
        y = np.interp(domain, self.x, self.y)
        obj = Curve(np.stack((domain, y), axis=1), **self.__dict__['metadata'])
        return obj

    def rebinned(self, step=0.1, fixp=0):
        '''
        Provides effective way to compute new domain basing on step and fixp parameters.
        Then using change_domain() method to create new object with calculated domain and returns it.

        fixp doesn't have to be inside orginal domain.

        Return domain of a new curve specified by fixp=0 and step=1 and another Curve object:
        >>> print(Curve([[0,0], [5, 5], [10, 0]]).rebinned(1,0).x)
        [  0.   1.   2.   3.   4.   5.   6.   7.   8.   9.  10.]

        :param step: step size of new domain
        :param fixp: fixed point one of the points in new domain
        :return: new Curve object with domain specified by step and fixp parameters
        '''
        a, b = (np.min(self.x), np.max(self.x))
        count_start = abs(fixp - a) / step
        count_stop = abs(fixp - b) / step

        # depending on position of fixp with respect to the orginal domain
        # may be 1 of 3 cases:

        if fixp < a:
            count_start = math.ceil(count_start)
            count_stop = math.floor(count_stop)
        elif fixp > b:
            count_start = -math.floor(count_start)
            count_stop = -math.ceil(count_stop)
        else:
            count_start = -count_start
            count_stop = count_stop

        domain = [fixp + n * step for n in range(int(count_start), int(count_stop)+1)]
        return self.change_domain(domain)

    def __str__(self):
        ret = "shape: {}".format(self.shape) + \
              "\nX : [{:4.3f},{:4.3f}]".format(min(self.x), max(self.x)) + \
              "\nY : [{:4.6f},{:4.6f}]".format(min(self.y), max(self.y)) + \
              "\nMetadata : " + str(self.metadata)
        return ret


def main():
    c = Curve([[0, 0], [5, 5], [10, 0]])
    print("X:", c.x)
    print("Y:", c.y)
    for x in (0.5, 1, 1.5, 2.0, 4.5):
        print("x=", x, "y=", c.y_at_x(x))

    print('\n', '*'*30, 'Metadata testing\n')

    k = Curve([[0, 1], [1, 2], [2, 3], [4, 0]], meta1='example 1', meta2='example 2')
    print('X:', k.x)
    print('Y:', k.y)
    print('M:', k.metadata)

    print('\n__str__:\n', k)
    print('Futher tests:\n')

    k2 = k.view(np.ndarray)
    print(k2)

    k3 = k[1:2,:]
    print(k3)

    k2 = k.view(np.ndarray)
    print(k2)

    k3 = k[1:2,:]
    print(k3)

    print("X:", k.x)
    print("Y:", k.y)
    test = k.rebinned(0.7, -1)
    print("X:", test.x)
    print("Y:", test.y)
    print('M:', test.metadata)


    k2 = k.view(np.ndarray)
    print(k2)

    k3 = k[1:2,:]
    print(k3)


if __name__ == '__main__':
    main()
