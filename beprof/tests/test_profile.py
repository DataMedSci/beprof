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


class TestProfileXatY(TestCase):
    """
    Testing Profile.x_at_y()
    """
    def setUp(self):
        self.p = Profile([[0.0, 5.0], [0.1, 10.0], [0.2, 20.0], [0.3, 10.0]])

    def test_outside_points(self):
        # points outside profile range [5.0, 20.0]
        self.assertTrue(np.isnan(self.p.x_at_y(-1.0)))
        self.assertTrue(np.isnan(self.p.x_at_y(4.9999999)))
        self.assertTrue(np.isnan(self.p.x_at_y(20.0000001)))
        self.assertTrue(np.isnan(self.p.x_at_y(7.5, reverse=True)))

    def test_known_points(self):
        self.assertAlmostEqual(self.p.x_at_y(5.0), 0.0)
        self.assertAlmostEquals(self.p.x_at_y(10.0), 0.1)
        self.assertAlmostEquals(self.p.x_at_y(20.0), 0.2)
        self.assertAlmostEquals(self.p.x_at_y(20.0, reverse=True), 0.2)
        self.assertAlmostEquals(self.p.x_at_y(10.0, reverse=True), 0.3)

    def test_between_known_points(self):
        # some points between known ones
        self.assertAlmostEquals(self.p.x_at_y(7.5), 0.05)
        self.assertAlmostEquals(self.p.x_at_y(11.11), 0.1111)
        self.assertAlmostEquals(self.p.x_at_y(19.99), 0.1999)
        self.assertAlmostEquals(self.p.x_at_y(19.99, reverse=True), 0.2001)

    def test_exceptioons(self):
        with self.assertRaises(TypeError):
            self.p.x_at_y()
        with self.assertRaises(TypeError):
            self.p.x_at_y('a')


class TestProfileWidth(TestCase):
    """
    Testing Profile.width()
    """
    def setUp(self):
        self.p = Profile([[0.0, 5.0], [0.1, 10.0], [0.2, 20.0], [0.3, 10.0]])

    def test_out_of_range_width(self):
        # out of range
        self.assertTrue(np.isnan(self.p.width(0.0)))
        self.assertTrue(np.isnan(self.p.width(5.0)))
        self.assertTrue(np.isnan(self.p.width(9.9)))
        self.assertTrue(np.isnan(self.p.width(20.1)))
        self.assertTrue(np.isnan(self.p.width(25.0)))

    def test_in_range_width(self):
        self.assertAlmostEquals(self.p.width(10.0), 0.2)
        self.assertAlmostEquals(self.p.width(15.0), 0.1)
        self.assertAlmostEquals(self.p.width(20.0), 0.0)  # only one point (0, 20)

    def test_width_exceptions(self):
        with self.assertRaises(TypeError):
            self.p.width()
        with self.assertRaises(TypeError):
            self.p.width('a')


class TestProfileFWHM(TestCase):
    """
    Testing Profile.fwhm
    """
    def setUp(self):
        self.p = Profile([[0.0, 5.0], [0.1, 10.0], [0.2, 20.0], [0.3, 10.0]])

    def test_basic_fwhm(self):
        p1 = Profile([[1, 1], [2, 2], [3, 1]])
        self.assertAlmostEquals(p1.fwhm, 2)
        p2 = Profile([[-12, 1], [-1, 17], [0, 3], [3, 1]])
        self.assertAlmostEquals(p2.fwhm, 6.45089, 5)

    def test_outside_range_fwhm(self):
        p3 = Profile([[-12, 1], [-1, 7], [0, 3], [3, 17]])
        self.assertTrue(np.isnan(p3.fwhm))

    def test_fwhm_exception(self):
        # objects in not callable
        with self.assertRaises(TypeError):
            self.p.fwhm()


class TestProfileNormalize(TestCase):
    """
    Testing Profile.normalize()
    """
    def setUp(self):
        self.p = Profile([[0.0, 5.0], [1, 10.0], [2, 15.0], [3, 10.0]])
        self.p_int = Profile([[1, 1], [2, 2], [3, 3], [4, 2], [5, 1]], dtype=np.int)

    def test_basic_normalize_by_one(self):
        self.p.normalize(1)
        self.assertTrue(np.allclose(self.p.y, [0.666666, 1.333333, 2., 1.333333]))

    def test_basic_normalize_by_two(self):
        self.p.normalize(2)
        self.assertTrue(np.allclose(self.p.y, [0.5, 1., 1.5, 1.]))

    def test_normalize_integers(self):
        # Testing normalization of integer-filled profiles
        # case 1 - int filled 'p_int /= dt' raises:
        # TypeError: ufunc 'true_divide' output (typecode 'd') could not be coerced to provided output
        # parameter (typecode 'l') according to the casting rule ''same_kind''
        with self.assertRaises(TypeError):
            self.p_int.normalize(1, allow_cast=False)
        # case 2 - we allow p_int = p_int / dt
        # division in place error is logged when trying to do 'p_int /= dt'
        self.p_int.normalize(1, allow_cast=True)
        self.assertTrue(np.array_equal(self.p_int.y, [1, 2, 3, 2, 1]))
        # values in p_int are integers
        self.assertTrue(np.issubdtype(self.p_int.dtype, int))

    def test_normalize_integers_by_float(self):
        # dtype==int preserved
        self.p_int.normalize(2.2, allow_cast=True)
        self.assertTrue(np.array_equal(self.p_int.y, [0, 1, 2, 1, 0]))
        self.assertTrue(np.issubdtype(self.p_int.dtype, int))
        # but if we do not allow cast:
        with self.assertRaises(TypeError):
            self.p_int.normalize(2.2, allow_cast=False)

    def test_normalize_exception(self):
        # case - less or equal to 0
        with self.assertRaises(ValueError):
            self.p.normalize(0)
        with self.assertRaises(ValueError):
            self.p.normalize(-1)
