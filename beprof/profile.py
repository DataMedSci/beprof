from beprof import curve
from beprof import functions
import numpy as np
import logging

__author__ = 'grzanka'

logger = logging.getLogger(__name__)


class Profile(curve.Curve):
    """
    General profile characterized by rising and falling edge.
    """

    def __new__(cls, input_array, axis=None, **meta):
        logger.info('Creating Profile object, metadata is: %s', meta)
        # input_array shape control provided in Curve class
        new = super(Profile, cls).__new__(cls, input_array, **meta)
        if axis is None:
            new.axis = getattr(input_array, 'axis', None)
        else:
            new.axis = axis
        return new

    def __array_finalize__(self, obj):
        if obj is None:
            return
        self.metadata = getattr(obj, 'metadata', {})

    def x_at_y(self, y, reverse=False):
        """
        Calculates inverse profile - for given y returns x such that f(x) = y
        If given y is not found in the self.y, then interpolation is used.
        By default returns first result looking from left,
        if reverse argument set to True,
        looks from right. If y is outside range of self.y
        then np.nan is returned.

        Use inverse lookup to get x-coordinate of first point:
        >>> float(Profile([[0.0, 5.0], [0.1, 10.0], [0.2, 20.0], [0.3, 10.0]])\
            .x_at_y(5.))
        0.0

        Use inverse lookup to get x-coordinate of second point,
        looking from left:
        >>> float(Profile([[0.0, 5.0], [0.1, 10.0], [0.2, 20.0], [0.3, 10.0]])\
            .x_at_y(10.))
        0.1

        Use inverse lookup to get x-coordinate of fourth point,
        looking from right:
        >>> float(Profile([[0.0, 5.0], [0.1, 10.0], [0.2, 20.0], [0.3, 10.0]])\
            .x_at_y(10., reverse=True))
        0.3

        Use interpolation between first two points:
        >>> float(Profile([[0.0, 5.0], [0.1, 10.0], [0.2, 20.0], [0.3, 10.0]])\
            .x_at_y(7.5))
        0.05

        Looking for y below self.y range:
        >>> float(Profile([[0.0, 5.0], [0.1, 10.0], [0.2, 20.0], [0.3, 10.0]])\
            .x_at_y(2.0))
        nan

        Looking for y above self.y range:
        >>> float(Profile([[0.0, 5.0], [0.1, 10.0], [0.2, 20.0], [0.3, 10.0]])\
            .x_at_y(22.0))
        nan

        :param y: reference value
        :param reverse: boolean value - direction of lookup
        :return: x value corresponding to given y or NaN if not found
        """
        logger.info('Running %(name)s.y_at_x(y=%(y)s, reverse=%(rev)s)',
                    {"name": self.__class__, "y": y, "rev": reverse})
        # positive or negative direction handles
        x_handle, y_handle = self.x, self.y
        if reverse:
            x_handle, y_handle = self.x[::-1], self.y[::-1]

        # find the index of first value in self.y greater or equal than y
        cond = y_handle >= y
        ind = np.argmax(cond)

        # two boundary conditions where x cannot be found:
        # A) y > max(self.y)
        # B) y < min(self.y)

        # A) if y > max(self.y) then condition self.y >= y
        #   will never be satisfied
        #   np.argmax( cond ) will be equal 0  and  cond[ind] will be False
        if not cond[ind]:
            return np.nan

        # B) if y < min(self.y) then condition self.y >= y
        #   will be satisfied on first item
        #   np.argmax(cond) will be equal 0,
        #   to exclude situation that y_handle[0] = y
        #   we also check if y < y_handle[0]
        if ind == 0 and y < y_handle[0]:
            return np.nan

        # use lookup if y in self.y:
        if cond[ind] and y_handle[ind] == y:
            return x_handle[ind]

        # alternatively - pure python implementation
        # return x_handle[ind] - \
        #        ((x_handle[ind] - x_handle[ind - 1]) / \
        #        (y_handle[ind] - y_handle[ind - 1])) * \
        #        (y_handle[ind] - y)

        # use interpolation
        sl = slice(ind - 1, ind + 1)
        return np.interp(y, y_handle[sl], x_handle[sl])

    def width(self, level):
        """
        Width at given level
        :param level:
        :return:
        """
        return self.x_at_y(level, reverse=True) - self.x_at_y(level)

    @property
    def fwhm(self):
        """
        Full width af half-maximum
        :return:
        """
        return self.width(0.5 * np.max(self.y))

    def normalize(self, dt, allow_cast=True):
        """
        Normalize to 1 over [-dt, +dt] area, if allow_cast is set
        to True, division not in place and casting may occur.
        If division in place is not possible and allow_cast is False
        an exception is raised.

        >>> a = Profile([[0, 0], [1, 5], [2, 10], [3, 5], [4, 0]])
        >>> a.normalize(1, allow_cast=True)
        >>> print(a.y)
        [0. 2. 4. 2. 0.]

        :param dt:
        :param allow_cast:
        """
        if dt <= 0:
            raise ValueError("Expected positive input")
        logger.info('Running %(name)s.normalize(dt=%(dt)s)', {"name": self.__class__, "dt": dt})
        try:
            ave = np.average(self.y[np.fabs(self.x) <= dt])
        except RuntimeWarning as e:
            logger.error('in normalize(). self class is %(name)s, dt=%(dt)s', {"name": self.__class__, "dt": dt})
            raise Exception("Scaling factor error: {0}".format(e))
        try:
            self.y /= ave
        except TypeError as e:
            logger.warning("Division in place is impossible: %s", e)
            if allow_cast:
                self.y = self.y / ave
            else:
                logger.error("Division in place impossible - allow_cast flag set to True should help")
                raise

    def __str__(self):
        logger.info('Running %s.__str__', self.__class__)
        ret = curve.Curve.__str__(self)
        ret += "\nFWHM = {:2.3f}".format(self.fwhm)
        return ret


def main():
    print('\nProfile')
    p = Profile([[0, 0], [1, 1], [2, 2], [3, 1]], some='exemplary', meta='data')
    print(p)
    print(type(p))
    print("X:", p.x)
    print("Y:", p.y)
    print('M: ', p.metadata)

    p2 = Profile([[1.5, 1], [2.5, 1], [3.5, 2], [4, 1]])
    print("X:", p2.x)
    print("Y:", p2.y)
    print('M: ', p2.metadata)

    b = curve.Curve([[0.5, 1], [1.5, 1], [2, 1], [2.5, 1]], negative='one')

    print('\na: \n')
    print('X: ', b.x)
    print('Y: ', b.y)
    print('M: ', b.metadata)

    diff = functions.subtract(p, b)
    print('type(diff): ', type(diff))
    print("X:", diff.x)
    print("Y:", diff.y)
    print('M: ', diff.metadata)


if __name__ == '__main__':
    main()
