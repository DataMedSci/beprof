import numpy as np
import unittest
from beprof.curve import Curve


class TestCurveInit(unittest.TestCase):
    """
    Testing Curve initialization and .x .y
    """

    def test_list_init(self):
        simple_lists = [[-12, 1], [-1, 7], [0, 3], [3, 17]]
        c = Curve(simple_lists)
        assert np.array_equal(c, simple_lists)

    def test_numpy_array_init(self):
        numpy_array = np.array([[-12, 1], [-1, 7], [0, 3], [3, 17]])
        c = Curve(numpy_array)
        assert np.array_equal(c, numpy_array)

    def test_numpy_view_init(self):
        # todo
        pass

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
        assert np.array_equal(c, array)

    def test_nonnumerical_init(self):
        # todo: we need to investigate this
        with self.assertRaises(IndexError):
            Curve(['a', 'b'])
        self.assertEquals(Curve([['a', 'b']]).x, ['a'])


class TestCurveRescale(unittest.TestCase):
    def setUp(self):
        # two the same Curves - one for modification/testing,
        # one for comparison (unmodified)
        self.compare_curve = Curve([[0, 0], [5, 5], [10, 10]])
        self.test_curve = Curve([[0.0, 0], [5, 5], [10, 10]])

    def test_rescale_by_one(self):
        self.test_curve.rescale(factor=1)
        assert np.array_equal(self.compare_curve, self.test_curve)

    def test_rescale_by_negative_one(self):
        self.test_curve.rescale(factor=-1)
        assert np.array_equal(self.compare_curve.x, self.test_curve.x)
        assert np.array_equal(self.compare_curve.y, (self.test_curve.y * -1))

    def test_rescale_by_zero(self):
        # post.y should contain some nans and infs
        self.test_curve.rescale(factor=0)
        assert np.array_equal(self.compare_curve.x, self.test_curve.x)
        assert np.isnan(self.test_curve.y[0])
        assert np.isinf(self.test_curve.y[1])
        assert np.isinf(self.test_curve.y[2])


class TestCurveSmooth(unittest.TestCase):
    def setUp(self):
        # two the same Curves - one for modification/testing,
        # one for comparison (unmodified)
        self.compare_curve = Curve([
            [0, 0], [1, 5], [2, 0], [3, 0], [4, -10], [5, 0]
        ])
        self.test_curve = Curve([
            [0, 0], [1, 5], [2, 0], [3, 0], [4, -10], [5, 0]
        ])

    def test_smooth_with_window_one(self):
        self.test_curve.smooth(window=1)
        assert np.array_equal(self.compare_curve.x, self.test_curve.x)
        assert np.array_equal(self.compare_curve.y, self.test_curve.y)

    def test_smooth_with_negative_window(self):
        with self.assertRaises(ValueError):
            self.test_curve.smooth(window=-1)

    def test_smooth_with_window_zero(self):
        with self.assertRaises(ValueError):
            self.test_curve.smooth(window=0)


class TestCurve(unittest.TestCase):
    def setUp(self):
        self.c = Curve([[0, 0], [5, 5], [10, 0]])

    def test_y_at_x(self):
        assert np.isnan(self.c.y_at_x(-12))  # outside domain, left
        self.assertEqual(self.c.y_at_x(2.5), 2.5)  # in domain
        self.assertEqual(self.c.y_at_x(6.7), 3.3)
        assert np.isnan(self.c.y_at_x(12))  # outside domain, right
        # test existing points in Curve
        self.assertEqual(self.c.y_at_x(0), 0)
        self.assertEqual(self.c.y_at_x(0.0), 0)
        self.assertEqual(self.c.y_at_x(-0.0), 0)  # 'negative zero'
        self.assertEqual(self.c.y_at_x(5), 5)
        self.assertEqual(self.c.y_at_x(10), 0)

    def test_change_domain(self):
        # one point
        assert np.array_equal(self.c.change_domain([7]).y, [3])
        # two points
        assert np.array_equal(self.c.change_domain([3, 7]).y, [3, 3])
        # more than previously
        assert np.array_equal(self.c.change_domain([1, 2, 3, 4, 5, 6, 7, 8]).y,
                              [1, 2, 3, 4, 5, 4, 3, 2]
                              )
        with self.assertRaises(ValueError):
            # outside domain
            self.c.change_domain([12])
            self.c.change_domain([-12])

    # def test_rebinned(self):
    #     self.fail()
    #
    # def test_evaluate_at_x(self):
    #     self.fail()
    #
    # def test_subtract(self):
    #     self.fail()
