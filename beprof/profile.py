from beprof.curve import Curve
import numpy as np
import beprof.functions

__author__ = 'grzanka'


class Profile(Curve):
    """
    General profile characterized by rising and falling edge
    Might be depth profile (along Z axis) or lateral profile (X or Y scan)
    """

    def __new__(cls, input_array, **kwargs):
        new = super().__new__(cls, input_array, **kwargs)
        return new

    def __array_finalize__(self, obj):
        # print("Here I am in Profile.__array_finalize__ obj: ", type(obj))
        if obj is None:
            return
        self.metadata = getattr(obj, 'metadata', {})

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
        try:
            ave = np.average(self.y[np.fabs(self.x) <= dt])
        except RuntimeWarning as e:
            raise Exception("Scaling factor is " + str(ave)) from e
        self.y /= ave

    def __str__(self):
        ret = super().__str__()
        ret += "\n FWHM = {:2.3f}".format(self.fwhm)
        return ret


class LateralProfile(Profile):
    def __new__(cls, input_array, **kwargs):
        new = super().__new__(cls, input_array, **kwargs)
        return new

    def __array_finalize__(self, obj):
        # print("Here I am in LateralProfile.__array_finalize__ obj: ", type(obj))
        if obj is None:
            return
        self.metadata = getattr(obj, 'metadata', {})

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
    p = Profile([[0, 0], [1, 1], [2, 2], [3, 1]], some='exapmlary', meta='data')
    print("X:", p.x)
    print("Y:", p.y)
    print('M: ', p.metadata)

    p2 = Profile([[1.5, 1], [2.5, 1], [3.5, 2], [4, 1]])
    print("X:", p2.x)
    print("Y:", p2.y)
    print('M: ', p2.metadata)

    b = Curve([[0.5, 1], [1.5, 1], [2, 1], [2.5, 1]], negative='one')

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
