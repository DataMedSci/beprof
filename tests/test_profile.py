import unittest

import numpy as np

from beprof.profile import Profile


class TestProfileInit(unittest.TestCase):
    """
    Testing Profile initialization
    """

    def test_list_init(self):
        simple_lists = [[-12, 1], [-1, 7], [0, 3], [3, 17]]
        p = Profile(simple_lists)
        assert np.array_equal(p, simple_lists)

    def test_numpy_array_init(self):
        numpy_array = np.array([[-12, 1], [-1, 7], [0, 3], [3, 17]])
        p = Profile(numpy_array)
        assert np.array_equal(p, numpy_array)

    def test_numpy_view_init(self):
        numpy_array = np.array([[-12, 1], [-1, 7], [0, 3], [3, 17]])
        p = Profile(numpy_array.view())
        assert np.array_equal(p, numpy_array)

    def test_empty_init(self):
        with self.assertRaises(TypeError):
            Profile()
        with self.assertRaises(IndexError):
            Profile([])
        with self.assertRaises(IndexError):
            Profile([[]])

    def test_one_point_init(self):
        p = Profile([[1, 2]])
        self.assertEqual(p.x, 1)
        self.assertEqual(p.y, 2)

    def test_two_point_init(self):
        array = [[-1, 3], [1, 7]]
        p = Profile(array)
        assert np.array_equal(p, array)

    def test_nonnumerical_init(self):
        with self.assertRaises(IndexError):
            Profile(['a', 'b'])
        assert np.array_equal(Profile([['a', 'b']]).x, ['a'])


class TestProfile(unittest.TestCase):
    """
    Testing Profile specific methods
    """

    def test_x_at_y(self):
        p = Profile([[0.0, 5.0], [0.1, 10.0], [0.2, 20.0], [0.3, 10.0]])
        # points outside profile range [5.0, 20.0]
        assert np.isnan(p.x_at_y(-1.0))
        assert np.isnan(p.x_at_y(4.9999999))
        assert np.isnan(p.x_at_y(20.0000001))
        assert np.isnan(p.x_at_y(7.5, reverse=True))
        # known points
        self.assertAlmostEqual(p.x_at_y(5.0), 0.0)
        self.assertAlmostEquals(p.x_at_y(10.0), 0.1)
        self.assertAlmostEquals(p.x_at_y(20.0), 0.2)
        self.assertAlmostEquals(p.x_at_y(20.0, reverse=True), 0.2)
        self.assertAlmostEquals(p.x_at_y(10.0, reverse=True), 0.3)
        # some points between known ones
        self.assertAlmostEquals(p.x_at_y(7.5), 0.05)
        self.assertAlmostEquals(p.x_at_y(11.11), 0.1111)
        self.assertAlmostEquals(p.x_at_y(19.99), 0.1999)
        self.assertAlmostEquals(p.x_at_y(19.99, reverse=True), 0.2001)
        # basic exception testing
        with self.assertRaises(TypeError):
            p.x_at_y()
        with self.assertRaises(TypeError):
            p.x_at_y('a')

    def test_width(self):
        p = Profile([[0.0, 5.0], [0.1, 10.0], [0.2, 20.0], [0.3, 10.0]])
        # out of range
        assert np.isnan(p.width(0.0))
        assert np.isnan(p.width(5.0))
        assert np.isnan(p.width(9.9))
        assert np.isnan(p.width(20.1))
        assert np.isnan(p.width(25.0))
        # in range
        self.assertAlmostEquals(p.width(10.0), 0.2)
        self.assertAlmostEquals(p.width(15.0), 0.1)
        self.assertAlmostEquals(p.width(20.0), 0.0)  # only one point (0, 20)
        # some exception testing
        with self.assertRaises(TypeError):
            p.width()
        with self.assertRaises(TypeError):
            p.width('a')

    def test_fwhm(self):
        p1 = Profile([[1, 1], [2, 2], [3, 1]])
        self.assertAlmostEquals(p1.fwhm, 2)
        p2 = Profile([[-12, 1], [-1, 17], [0, 3], [3, 1]])
        self.assertAlmostEquals(p2.fwhm, 6.45089, 5)
        # should go out of range
        p3 = Profile([[-12, 1], [-1, 7], [0, 3], [3, 17]])
        assert np.isnan(p3.fwhm)

    def test_normalize(self):
        pass
