from unittest import TestCase

import numpy as np

from beprof.profile import Profile


class TestProfileInit(TestCase):
    """
    Testing Profile initialization
    """
    def setUp(self):
        self.simple_lists = ([-12, 1], [-1, 7], [0, 3], [3, 17])

    def test_list_init(self):
        p = Profile(self.simple_lists)
        self.assertTrue(np.array_equal(p, self.simple_lists))

    def test_numpy_array_init(self):
        numpy_array = np.array(self.simple_lists)
        p = Profile(numpy_array)
        self.assertTrue(np.array_equal(p, numpy_array))

    def test_numpy_view_init(self):
        numpy_array = np.array(self.simple_lists)
        p = Profile(numpy_array.view())
        self.assertTrue(np.array_equal(p, numpy_array))

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
        self.assertTrue(np.array_equal(p, array))

    def test_nonnumerical_init(self):
        with self.assertRaises(ValueError):
            Profile([['a', 'b']])
        with self.assertRaises(ValueError):
            Profile([['a', 1], [0.2, 'b']])


class TestProfile(TestCase):
    """
    Testing Profile specific methods
    """
    def setUp(self):
        self.p = Profile([[0.0, 5.0], [0.1, 10.0], [0.2, 20.0], [0.3, 10.0]])

    def test_x_at_y(self):
        # points outside profile range [5.0, 20.0]
        self.assertTrue(np.isnan(self.p.x_at_y(-1.0)))
        self.assertTrue(np.isnan(self.p.x_at_y(4.9999999)))
        self.assertTrue(np.isnan(self.p.x_at_y(20.0000001)))
        self.assertTrue(np.isnan(self.p.x_at_y(7.5, reverse=True)))
        # known points
        self.assertAlmostEqual(self.p.x_at_y(5.0), 0.0)
        self.assertAlmostEquals(self.p.x_at_y(10.0), 0.1)
        self.assertAlmostEquals(self.p.x_at_y(20.0), 0.2)
        self.assertAlmostEquals(self.p.x_at_y(20.0, reverse=True), 0.2)
        self.assertAlmostEquals(self.p.x_at_y(10.0, reverse=True), 0.3)
        # some points between known ones
        self.assertAlmostEquals(self.p.x_at_y(7.5), 0.05)
        self.assertAlmostEquals(self.p.x_at_y(11.11), 0.1111)
        self.assertAlmostEquals(self.p.x_at_y(19.99), 0.1999)
        self.assertAlmostEquals(self.p.x_at_y(19.99, reverse=True), 0.2001)
        # basic exception testing
        with self.assertRaises(TypeError):
            self.p.x_at_y()
        with self.assertRaises(TypeError):
            self.p.x_at_y('a')

    def test_width(self):
        # out of range
        self.assertTrue(np.isnan(self.p.width(0.0)))
        self.assertTrue(np.isnan(self.p.width(5.0)))
        self.assertTrue(np.isnan(self.p.width(9.9)))
        self.assertTrue(np.isnan(self.p.width(20.1)))
        self.assertTrue(np.isnan(self.p.width(25.0)))
        # in range
        self.assertAlmostEquals(self.p.width(10.0), 0.2)
        self.assertAlmostEquals(self.p.width(15.0), 0.1)
        self.assertAlmostEquals(self.p.width(20.0), 0.0)  # only one point (0, 20)
        # some exception testing
        with self.assertRaises(TypeError):
            self.p.width()
        with self.assertRaises(TypeError):
            self.p.width('a')

    def test_fwhm(self):
        p1 = Profile([[1, 1], [2, 2], [3, 1]])
        self.assertAlmostEquals(p1.fwhm, 2)
        p2 = Profile([[-12, 1], [-1, 17], [0, 3], [3, 1]])
        self.assertAlmostEquals(p2.fwhm, 6.45089, 5)
        # should go out of range
        p3 = Profile([[-12, 1], [-1, 7], [0, 3], [3, 17]])
        self.assertTrue(np.isnan(p3.fwhm))
        # it is not callable
        with self.assertRaises(TypeError):
            self.p.fwhm()

    def test_normalize(self):
        p1 = Profile([[1, 1], [2, 20], [3, 40]])
        p1.normalize(1)
        self.assertTrue(np.array_equal(p1.y, [1, 20, 40]))

        p1 = Profile([[1, 1], [2, 2], [3, 3], [4, 2], [5, 1]])
        p1.normalize(2)
        self.assertTrue(np.allclose(p1.y, [0.666666, 1.333333, 2, 1.333333, 0.666666]))

        # case - less or equal to 0
        with self.assertRaises(ValueError):
            p1.normalize(0)
        with self.assertRaises(ValueError):
            p1.normalize(-1)
