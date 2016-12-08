import numpy as np

from unittest import TestCase

from beprof.curve import Curve


class TestCurveInit(TestCase):
    """
    Testing Curve initialization and .x .y
    """

    def test_list_init(self):
        simple_lists = [[-12, 1], [-1, 7], [0, 3], [3, 17]]
        c = Curve(simple_lists)
        self.assertTrue(np.array_equal(c, simple_lists))

    def test_numpy_array_init(self):
        numpy_array = np.array([[-12, 1], [-1, 7], [0, 3], [3, 17]])
        c = Curve(numpy_array)
        self.assertTrue(np.array_equal(c, numpy_array))

    def test_numpy_view_init(self):
        numpy_array = np.array([[-12, 1], [-1, 7], [0, 3], [3, 17]])
        p = Curve(numpy_array.view())
        self.assertTrue(np.array_equal(p, numpy_array))

    def test_empty_init(self):
        with self.assertRaises(TypeError):
            Curve()
        with self.assertRaises(IndexError):
            Curve([])
        with self.assertRaises(IndexError):
            Curve([[]])

    def test_one_point_init(self):
        c = Curve([[1, 2]])
        self.assertEqual(c.x, 1)
        self.assertEqual(c.y, 2)

    def test_two_point_init(self):
        array = [[-1, 3], [1, 7]]
        c = Curve(array)
        self.assertTrue(np.array_equal(c, array))

    def test_nonnumerical_init(self):
        with self.assertRaises(ValueError):
            Curve([['a', 'b']])
        with self.assertRaises(ValueError):
            Curve([['a', 1], [0.2, 'b']])


class TestCurveRescale(TestCase):
    def setUp(self):
        # two the same Curves - one for modification/testing,
        # one for comparison (unmodified)
        self.compare_curve = Curve([[0, 0], [5, 5], [10, 10]])
        self.test_curve = Curve([[0.0, 0], [5, 5], [10, 10]])

    def test_rescale_by_one(self):
        self.test_curve.rescale(factor=1)
        self.assertTrue(np.array_equal(self.compare_curve, self.test_curve))

    def test_rescale_by_negative_one(self):
        self.test_curve.rescale(factor=-1)
        self.assertTrue(np.array_equal(self.compare_curve.x, self.test_curve.x))
        self.assertTrue(np.array_equal(self.compare_curve.y, (self.test_curve.y * -1)))

    def test_rescale_by_zero(self):
        # post.y should contain some nans and infs
        self.test_curve.rescale(factor=0)
        self.assertTrue(np.array_equal(self.compare_curve.x, self.test_curve.x))
        self.assertTrue(np.isnan(self.test_curve.y[0]))
        self.assertTrue(np.isinf(self.test_curve.y[1]))
        self.assertTrue(np.isinf(self.test_curve.y[2]))


class TestCurveSmooth(TestCase):
    def setUp(self):
        # two the same Curves - one for modification/testing,
        # one for comparison (unmodified)
        self.compare_curve = Curve([[0, 0], [1, 5], [2, 0], [3, 0], [4, -10], [5, 0]])
        self.test_curve = Curve([[0, 0], [1, 5], [2, 0], [3, 0], [4, -10], [5, 0]])

    def test_smooth_with_window_one(self):
        self.test_curve.smooth(window=1)
        self.assertTrue(np.array_equal(self.compare_curve.x, self.test_curve.x))
        self.assertTrue(np.array_equal(self.compare_curve.y, self.test_curve.y))

    def test_smooth_with_negative_window(self):
        with self.assertRaises(ValueError):
            self.test_curve.smooth(window=-1)
        with self.assertRaises(ValueError):
            self.test_curve.smooth(window=-3)

    def test_even_windows(self):
        with self.assertRaises(ValueError):
            self.test_curve.smooth(window=2)
        with self.assertRaises(ValueError):
            self.test_curve.smooth(window=4)
        with self.assertRaises(ValueError):
            self.test_curve.smooth(window=6)

    def test_odd_window(self):
        self.test_curve.smooth(window=3)
        self.assertTrue(np.array_equal(self.test_curve, [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0]]))
        self.test_curve = self.compare_curve.copy()
        self.test_curve.smooth(window=5)
        self.assertTrue(np.array_equal(self.test_curve, [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0]]))


class TestCurve(TestCase):
    def setUp(self):
        self.c = Curve([[0, 0], [5, 5], [10, 0]])

    def test_y_at_x(self):
        self.assertTrue(np.isnan(self.c.y_at_x(-12)))  # outside domain, left
        self.assertEqual(self.c.y_at_x(2.5), 2.5)  # in domain
        self.assertEqual(self.c.y_at_x(6.7), 3.3)
        self.assertTrue(np.isnan(self.c.y_at_x(12)))  # outside domain, right
        # test existing points in Curve
        self.assertEqual(self.c.y_at_x(0), 0)
        self.assertEqual(self.c.y_at_x(0.0), 0)
        self.assertEqual(self.c.y_at_x(-0.0), 0)  # 'negative zero'
        self.assertEqual(self.c.y_at_x(5), 5)
        self.assertEqual(self.c.y_at_x(10), 0)

    def test_change_domain(self):
        # one point
        self.assertTrue(np.array_equal(self.c.change_domain([7]).y, [3]))
        # two points
        self.assertTrue(np.array_equal(self.c.change_domain([3, 7]).y, [3, 3]))
        # more than previously
        self.assertTrue(np.array_equal(self.c.change_domain([1, 2, 3, 4, 5, 6, 7, 8]).y, [1, 2, 3, 4, 5, 4, 3, 2]))
        # outside domain
        with self.assertRaises(ValueError):
            self.c.change_domain([12])
        with self.assertRaises(ValueError):
            self.c.change_domain([-12])

    def test_rebinned(self):
        new_c = self.c.rebinned(step=1)
        self.assertTrue(np.array_equal(new_c.x, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))
        # todo: probably something wrong with fixp, they both throw ValueError
        # new_c = self.c.rebinned(step=2, fixp=15)
        # self.assertTrue(np.array_equal(new_c.x, [1, 3, 5, 7, 9]))
        # new_c = self.c.rebinned(step=2, fixp=-5)
        # self.assertTrue(np.array_equal(new_c.x, [-1, 1, 3, 5, 7, 9]))

    def test_evaluate_at_x(self):
        # test inside and outside domain
        self.assertTrue(np.array_equal(self.c.evaluate_at_x([-1, 0, 1, 10, 11], def_val=37), [37, 0, 1, 0, 37]))
        # test between existing points
        self.assertTrue(np.array_equal(self.c.evaluate_at_x([-0.333, 0.5, 0.7, 7.3], def_val=37), [37, 0.5, 0.7, 2.7]))

    def test_subtract(self):
        # c2 has wider domain than c1
        c1 = Curve([[-1, -1], [0, 0], [1, 5], [2, 0], [3, 0]])
        c2 = Curve([[-2, 1], [-1, 1], [0, 1], [1, 1], [2, 1], [3, 1], [4, 1]])

        # should return None and self
        self.assertIsNone(c1.subtract(c2, new_obj=False))
        self.assertTrue(np.array_equal(c1, [[-1, -2], [0, -1], [1, 4], [2, -1], [3, -1]]))
        # create new object and compare
        self.assertTrue(np.array_equal(c1.subtract(c2, new_obj=True), [[-1, -3], [0, -2], [1, 3], [2, -2], [3, -2]]))
