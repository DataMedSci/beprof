from enum import IntEnum
import numpy as np
import scipy
from scipy.interpolate import interp1d
from scipy import signal
import math
import copy
import beprof.functions


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
        if obj is None:
            return
        self.metadata = getattr(obj, 'metadata', None)

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
        obj = Curve(np.stack((domain, y), axis=1))
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

    def evaluate_at_x(self, arg, defval=0):
        y = np.interp(arg, self.x, self.y, left=defval, right=defval)
        return y
        
    def subtract(self, curve2, defval=0, newobj=True, domain='keep'):
        '''

        :param curve2: An object with which the difference will be computed
        :param defval: default value for points of curves that are out of domains intersection
        :param newobj: If True, a new object will be created. Else method will try to modify self
        :param domain: 'keep' if you want to keep the orginal domain of self,
                       'extend' if you want to add points form curve2 to the new domain
        :return:       new object of type type(self) if newobj is True, modified self otherwise
        '''


        # WILL BE CHANGED !!!

        # domain1 = [a1, b1]
        # domain2 = [a2, b2]
        a1, b1 = np.min(self.x), np.max(self.x)
        a2, b2 = np.min(curve2.x), np.max(curve2.x)

        # first: if the user doesn't want to create a new object in memory, 2 possible options:
        if not newobj:
            if a2 >= a1 and b2 <= b1:
                # if the orginal domain includes c2 domain, subtraction can be done as follows:
                # as the output domain is gonna be self.x, the subtracted values should be
                # interpolated c2 values for every point that is in self.x and in section [a2, b2]
                # and defval for the others. Values to subtract can be calculated using np.interp:

                y = np.interp(self.x, curve2.x, curve2.y, left=defval, right=defval)
                # print('y: ', y, type(y))
                # print('Y: ', self.y, type(self.y))
                self.y =  self.y - y
                return
            else:
                # if the orginal domain doesn't include c2 domain there is nothing that can be done
                print('Error, can not subtract without creating new object')
                return

        # since the program is here, that means newobj is True
        # what means the method is not going to modify self but create new curve object instead
        #
        # the first thing: what should be the domain of a new object?
        # User can set domain parameter to:
        # 'keep' - new object domain is self.x
        # 'extend' - new object domain is sum of sets self.x, c2.x,
        #  and values of c2.y in self.x-c2.x and self.x in c2.x - self.x are defval

        # anyway, there are 3 main possibilities:
        # 1) domains are disjoint when a2>b1 or a1>b2
        if a2 > b1 or a1 > b2:
            #if user decides to keep the orignal domain, the new object should be as follows:
            if domain == 'keep':
                obj = copy.deepcopy(self)
                obj.y = obj.y - defval
                return obj
            # could be else here but there might be more possibilities in the future
            # if user wants to extend the domain, new domain is a union.
            if domain == 'extend':
                tmp1 = np.array(self.y) - defval        # new values for self.x are correspoding self.y-defval
                tmp2 = defval - np.array(curve2.y)          # new values for c2.x are corresponding defval - c2.y
                if a2 > b1:     # here we have ------a1||||||b1-----a2|||||b2------>
                    newX = np.concatenate((self.x, curve2.x))        # new X is just an union
                    newY = np.concatenate((tmp1, tmp2))    # into one list
                else:           # mirrored, just a minor change
                    newX = np.concatenate((curv2.x, self.x))        # new X is just an union
                    newY = np.concatenate((tmp2, tmp1))             # into one list

                print('newX: ', newX)
                print('newY: ', newY)
                obj = Curve(np.stack((newX, newY), axis=1), **self.__dict__['metadata'])
                return obj

    def __str__(self):
        ret = "shape: {}".format(self.shape) + \
              "\nX : [{:4.3f},{:4.3f}]".format(min(self.x), max(self.x)) + \
              "\nY : [{:4.6f},{:4.6f}]".format(min(self.y), max(self.y)) + \
              "\nMetadata : " + str(self.metadata)
        return ret


def main():

    print('\nSubtract method :\n')

    c = Curve([[0.0, 0], [5, 5], [10, 0]])
    print('c: \n', c)
    d = Curve([[0.0, 1], [5, 1], [10, 1]])
    print('d: \n', d)

    c.subtract(d, newobj=False)
    print('c-d: \n', c)
    print('*********')
    print('X:', c.x)
    print('Y:', c.y)

    print('Newobj creation #1\n\n')
    a = Curve([[0, 0], [1, 1], [2, 2], [3, 1]])
    b = Curve([[0.5, 1], [1.5, 1], [2, 1], [2.5, 1]])

    print('\na: \n')
    print('X: ', a.x)
    print('Y: ', a.y)


    print('\nb: \n')
    print('X: ', b.x)
    print('Y: ', b.y)


    diff = functions.subtract(a, b)
    print('\n diff: \n')
    print('X: ', diff.x)
    print('Y: ', diff.y)

    # print(diff.evaluate_at_x([-1, 0, 1, 1.5, 2, 3, 4]))



if __name__ == '__main__':
    main()
