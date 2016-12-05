import numpy as np
import math
import copy
from beprof import functions
import logging

logger = logging.getLogger(__name__)


class DataSet(np.ndarray):
    """
    1-D data set, used in type casting for X and Y component of Curve
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
    gathered data, extra information etc.

    One can add metadata to Curve object in 2 ways:
        1) When creating object, using extra arguments (**kwargs)
        2) When object (obj) already exists, one can use dictionary methods
           to add a field to obj.metadata dict.

    Raises:
        IndexError: this can happen when user is trying to create new Curve
                    object but uses incorrect array of points to initialise it.
                    Input array should be 2D or 3D (shape: (X, 2) or (X, 3)).
        ValueError: in change domain function: when the old domain
                    does not include the new one.
    """

    def __new__(cls, input_array, **meta):
        shape = np.shape(input_array)
        logger.info('Creating Curve object of shape {0} metadata is: {1}'.format(shape, meta))
        if shape[1] != 2 and shape[1] != 3:
            logger.error('Creating Curve object failed.'
                         'Input array must be an 2D or 3D array\n'
                         'np.shape(input_array_[1] must be either 2 or 3.')
            raise IndexError('Invalid format of input_array - ' 'shape is {0}, must be (X, 2) or (X, 3)'.format(shape))

        obj = np.asarray(input_array).view(cls)
        if meta is None:
            obj.metadata = {}
        else:
            obj.metadata = copy.deepcopy(meta)
        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return
        self.metadata = getattr(obj, 'metadata', {})

    @property
    def x(self):
        return self[:, 0].view(DataSet)

    @x.setter
    def x(self, value):
        self[:, 0] = value

    @property
    def y(self):
        return self[:, 1].view(DataSet)

    @y.setter
    def y(self, value):
        self[:, 1] = value

    def rescale(self, factor=1.0):
        self.y /= factor

    def smooth(self, window=3):
        self.y = functions.medfilt(self.y, window)

    def y_at_x(self, x):
        if x == self.x[0]:
            return x
        return np.interp(x, self.x, self.y, left=np.nan, right=np.nan)

    def change_domain(self, domain):
        """
        Creating new Curve object in memory with domain passed as a parameter.
        New domain must include in the original domain.
        Copies values from original curve and uses interpolation to calculate
        values for new points in domain.

        Calculate y - values of example curve with changed domain:
        >>> print(Curve([[0,0], [5, 5], [10, 0]])\
            .change_domain([1, 2, 8, 9]).y)
        [ 1.  2.  2.  1.]

        :param domain: set of points representing new domain.
            Might be a list or np.array.
        :return: new Curve object with domain set by 'domain' parameter
        """
        logger.info('Running {0}.change_domain() with new domain range:'
                    ' [{1}, {2}]'.format(self.__class__, np.min(domain), np.max(domain)))

        # check if new domain includes in the original domain
        if np.max(domain) > np.max(self.x) or np.min(domain) < np.min(self.x):
            logger.error('Old domain range: [{0}, {1}] does not include '
                         'new domain range: [{2}, {3}]'
                         .format(np.min(self.x), np.max(self.x), np.min(domain), np.max(domain)))
            raise ValueError('in change_domain():' 'the old domain does not include the new one')

        y = np.interp(domain, self.x, self.y)
        obj = self.__class__(np.stack((domain, y), axis=1), **self.__dict__['metadata'])
        return obj

    def rebinned(self, step=0.1, fixp=0):
        """
        Provides effective way to compute new domain basing on
        step and fixp parameters. Then using change_domain() method
        to create new object with calculated domain and returns it.

        fixp doesn't have to be inside original domain.

        Return domain of a new curve specified by
        fixp=0 and step=1 and another Curve object:
        >>> print(Curve([[0,0], [5, 5], [10, 0]]).rebinned(1, 0).x)
        [  0.   1.   2.   3.   4.   5.   6.   7.   8.   9.  10.]

        :param step: step size of new domain
        :param fixp: fixed point one of the points in new domain
        :return: new Curve object with domain specified by
            step and fixp parameters
        """
        logger.info('Running {0}.rebinned(step={1}, fixp={2})'.format(self.__class__, step, fixp))
        a, b = (np.min(self.x), np.max(self.x))
        count_start = abs(fixp - a) / step
        count_stop = abs(fixp - b) / step

        # depending on position of fixp with respect to the original domain
        # 3 cases may occur:
        if fixp < a:
            count_start = math.ceil(count_start)
            count_stop = math.floor(count_stop)
        elif fixp > b:
            count_start = -math.floor(count_start)
            count_stop = -math.ceil(count_stop)
        else:
            count_start = -count_start
            count_stop = count_stop

        domain = [fixp + n * step for n in range(int(count_start), int(count_stop) + 1)]
        return self.change_domain(domain)

    def evaluate_at_x(self, arg, def_val=0):
        """
        Returns Y value at arg of self. Arg can be a scalar,
        but also might be np.array or other iterable
        (like list). If domain of self is not wide enough to
        interpolate the value of Y, method will return
        def_val for those arguments instead.

        Check the interpolation when arg in domain of self:
        >>> Curve([[0, 0], [2, 2], [4, 4]]).evaluate_at_x([1, 2 ,3])
        array([ 1.,  2.,  3.])

        Check if behavior of the method is correct when arg
        id partly outside the domain:
        >>> Curve([[0, 0], [2, 2], [4, 4]]).evaluate_at_x(\
            [-1, 1, 2 ,3, 5], 100)
        array([ 100.,    1.,    2.,    3.,  100.])

        :param arg: x-value to calculate Y (may be an array or list as well)
        :param def_val: default value to return if can't interpolate at arg
        :return: np.array of Y-values at arg. If arg is a scalar,
            will return scalar as well
        """
        y = np.interp(arg, self.x, self.y, left=def_val, right=def_val)
        return y

    def subtract(self, curve2, new_obj=False):
        """
        Method that calculates difference between 2 curves
        (or subclasses of curves). Domain of self must be in
        domain of curve2 what means min(self.x) >= min(curve2.x)
        and max(self.x) <= max(curve2.x).
        Might modify self, and can return the result or None

        Use subtract as -= operator, check whether returned value is None:
        >>> Curve([[0, 0], [1, 1], [2, 2], [3, 1]]).subtract(\
            Curve([[-1, 1], [5, 1]])) is None
        True

        Use subtract again but return a new object this time.
        >>> Curve([[0, 0], [1, 1], [2, 2], [3, 1]]).subtract(\
            Curve([[-1, 1], [5, 1]]), new_obj=True).y
        DataSet([-1.,  0.,  1.,  0.])

        Try using wrong inputs to create a new object,
        and check whether it is None as expected:
        >>> Curve([[0, 0], [1, 1], [2, 2], [3, 1]]).subtract(\
            Curve([[1, -1], [2, -1]]), new_obj=True) is None
        True

        :param curve2: second object to calculate difference
        :param new_obj: if True, method is creating new object
            instead of modifying self
        :return: None if new_obj is False (but will modify self)
            or type(self) object containing the result
        """
        # domain1 = [a1, b1]
        # domain2 = [a2, b2]
        a1, b1 = np.min(self.x), np.max(self.x)
        a2, b2 = np.min(curve2.x), np.max(curve2.x)

        # check whether domain condition is satisfied
        if a2 > a1 or b2 < b1:
            logger.error('curve2 domain does not include self domain')
            # todo: raise exception
            return None
        # if we want to create and return a new object
        # rather then modify existing one
        if new_obj:
            return functions.subtract(self, curve2.change_domain(self.x))
        values = curve2.evaluate_at_x(self.x)
        self.y = self.y - values
        return None

    def __str__(self):
        logger.info('Running {0}.__str__'.format(self.__class__))
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

    c.subtract(d, new_obj=False)
    print('c-d: \n', c)
    print('*********')
    print('X:', c.x)
    print('Y:', c.y)

    print('Newobj creation #1\n\n')
    a = Curve([[0, 0], [1, 1], [2, 2], [3, 1]], positive='example')
    b = Curve([[0.5, 1], [1.5, 1], [2, 1], [2.5, 1]], negative='one')

    print('\na: \n')
    print('X: ', a.x)
    print('Y: ', a.y)
    print('M: ', a.metadata)

    print('\nb: \n')
    print('X: ', b.x)
    print('Y: ', b.y)
    print('M: ', b.metadata)

    diff = functions.subtract(a, b)
    print('\n diff: \n')
    print('X: ', diff.x)
    print('Y: ', diff.y)
    print('M: ', diff.metadata)
    # print(diff.evaluate_at_x([-1, 0, 1, 1.5, 2, 3, 4]))

    dif2 = b.subtract(a, True)
    print('\n dif2: \n')
    print('X: ', dif2.x)
    print('Y: ', dif2.y)
    print('M: ', dif2.metadata)

    print('\n b should be as before:\n')
    print('X: ', b.x)
    print('Y: ', b.y)
    print('M: ', b.metadata)

    print('\nNow calling b.subtract(a) what should change b' 'so that is looks like dif2')
    b.subtract(a)
    print('\nb: \n')
    print('X: ', b.x)
    print('Y: ', b.y)
    print('M: ', b.metadata)


if __name__ == '__main__':
    main()
