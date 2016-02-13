from beprof.curve import Curve
import numpy as np
import logging

__author__ = 'grzanka'


class Profile(Curve):
    """
    General profile characterized by rising and falling edge
    Might be depth profile (along Z axis) or lateral profile (X or Y scan)
    """

    def __new__(cls, input_array, axis=None, **meta):
        logging.info('Creating Profile object, metadata is: {0}'.format(meta))
        # input_array shape control provided in Curve class
        new = super().__new__(cls, input_array, **meta)
        if axis is None:
            new.axis = getattr(input_array,'axis',None)
        else:
            new.axis = axis
        return new

    def __array_finalize__(self, obj):
        if obj is None:
            return
        self.axis = getattr(obj, 'axis', None)

    def x_at_y(self, y, reverse=False):
        """
        Calculates inverse profile - for given y returns x such that f(x) = y
        If given y is not found in the self.y, then interpolation is used.
        By default returns first result looking from left, if reverse argument set to True, looks from right.
        If y is outside range of self.y then np.nan is returned.

        Use inverse lookup to get x-coordinate of first point:
        >>> float(Profile([[0.0, 5.0], [0.1, 10.0], [0.2, 20.0], [0.3, 10.0]]).x_at_y(5.))
        0.0

        Use inverse lookup to get x-coordinate of second point, looking from left:
        >>> float(Profile([[0.0, 5.0], [0.1, 10.0], [0.2, 20.0], [0.3, 10.0]]).x_at_y(10.))
        0.1

        Use inverse lookup to get x-coordinate of fourth point, looking from right:
        >>> float(Profile([[0.0, 5.0], [0.1, 10.0], [0.2, 20.0], [0.3, 10.0]]).x_at_y(10., reverse=True))
        0.3

        Use interpolation between first two points:
        >>> float(Profile([[0.0, 5.0], [0.1, 10.0], [0.2, 20.0], [0.3, 10.0]]).x_at_y(7.5))
        0.05

        Looking for y below self.y range:
        >>> float(Profile([[0.0, 5.0], [0.1, 10.0], [0.2, 20.0], [0.3, 10.0]]).x_at_y(2.0))
        nan

        Looking for y above self.y range:
        >>> float(Profile([[0.0, 5.0], [0.1, 10.0], [0.2, 20.0], [0.3, 10.0]]).x_at_y(22.0))
        nan

        :param y: reference value
        :param reverse: boolean value - direction of lookup
        :return: x value corresponding to given y or NaN if not found
        """
        logging.info('Running {0}.y_at_x(y={1}, reverse={2})'.format(self.__class__, y, reverse))
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

        # A) if y > max(self.y) then condition self.y >= y will never be satisfied
        # np.argmax( cond ) will be equal 0  and  cond[ind] will be False
        if not cond[ind]:
            return np.nan

        # B) if y < min(self.y) then condition self.y >= y will be satisfied on first item
        # np.argmax(cond) will be equal 0,
        # to exclude situation that y_handle[0] = y we also check if y < y_handle[0]
        if ind == 0 and y < y_handle[0]:
            return np.nan

        # use lookup if y in self.y:
        if cond[ind] and y_handle[ind] == y:
            return x_handle[ind]

        # alternatively - pure python implementation
        # return x_handle[ind] - \
        #        ((x_handle[ind] - x_handle[ind - 1]) / (y_handle[ind] - y_handle[ind - 1])) * \
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

    def normalize(self, dt):
        """
        Normalize to 1 over [-dt,+dt] area
        :param dt:
        :return:
        """
        logging.info('Running {0}.normalize(dt={1})'.format(self.__class__, dt))
        try:
            ave = np.average(self.y[np.fabs(self.x) <= dt])
        except RuntimeWarning as e:
            logging.error('in normalize(). self class is {0}, dt={1}'.format(self.__class__, dt))
            raise Exception("Scaling factor is " + str(ave)) from e
        self.y /= ave

    def __str__(self):
        logging.info('Running {0}.__str__'.format(self.__class__))
        ret = super().__str__()
        ret += "\n FWHM = {:2.3f}".format(self.fwhm)
        ret += " " + str(self.axis)
        return ret


class LateralProfile(Profile):
    def __new__(cls, input_array, axis=None, background=None, **meta):
        logging.info('Creating LateralProfile object, metadata is: {0}'.format(meta))
        # input_array shape control provided in Curve class
        new = super().__new__(cls, input_array, axis=axis, **meta)
        return new

    def __array_finalize__(self, obj):
        if obj is None:
            return
        self.axis = getattr(obj, 'axis', None)

    def left_penumbra(self, upper=0.9, lower=0.1):
        return self.x_at_y(upper) - self.x_at_y(lower)

    def right_penumbra(self, upper=0.9, lower=0.1):
        return self.x_at_y(lower, reverse=True) - self.x_at_y(upper, reverse=True)

    def center(self, level=0.5):
        return 0.5 * (self.x_at_y(level) + self.x_at_y(level, reverse=True))

    def mirror(self, m=0):
        """
        Provides mirror image of a profile with given Y axis (y=m).
        Domain of profile might be changed due to this operation.

        Use mirror() method to get values of mirrored profile:
        >>> lp = LateralProfile([[-1, 1], [0, -1], [1, 0]])
        >>> lp.mirror()
        >>> print(lp.y)
        [ 0 -1  1]

        :param m: Y value for mirror image.
        """
        self.x = 2*m - self.x
        self.x = self.x[::-1]
        self.y = self.y[::-1]

    def symmetrize(self):
        tmp = self.y[::-1].copy()
        self.y += tmp
        self.y /= 2.0

    def __str__(self):
        logging.info('Running {0}.__str__'.format(self.__class__))
        ret = super().__str__() + "\n"
        ret += "Center = {:2.3f}".format(self.center()) + \
               " Penumbra = [{:2.3f},{:2.3f}]".format(self.left_penumbra(), self.right_penumbra())
        return ret

    def __repr__(self):
        return str(self.__class__)


class DepthProfile(Profile):
    def range(self):
        # todo
        pass

    def maximum(self):
        # todo
        pass

    def plateau_to_max(self):
        # todo
        pass


def main():
    print('\nProfile')
    p = Profile([[1, 0], [2, 1], [3, 0]], first='one', second='two', third='three')
    print("X:", p.x)
    print("Y:", p.y)
    print("meta:", p.metadata)
    print(p)

    print('\nLateralProfile')
    lp = LateralProfile([[1, 0], [2, 1], [3, 0]], example='foo', anotherex='bar')
    print("X:", lp.x)
    print("Y:", lp.y)
    print("meta:", lp.metadata)
    print(lp)

    print('\nTEST:')
    test = lp.rebinned(0.5, 2)
    print('X:', test.x)
    print('Y:', test.y)
    print('M:', test.metadata)

    print(test)

    for x in (-1, 0, 0.5, 1, 1.5):
        print("x=", x, "y=", p.x_at_y(x), "rev", p.x_at_y(x, reverse=True))


if __name__ == '__main__':
    main()
