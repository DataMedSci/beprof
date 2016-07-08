import numpy as np
import pytest
import unittest
from beprof.curve import Curve


class TestCurveInit(unittest.TestCase):
    def test_list_init(self):
        simple_lists = [[-12, 1], [-1, 7], [0, 3], [3, 17]]
        c = Curve(simple_lists)
        print(list(c.x))
        assert list(c.x) == [e[0] for e in simple_lists]
        assert list(c.y) == [e[1] for e in simple_lists]

    def test_numpy_array_init(self):
        numpy_array = np.array([[-12, 1], [-1, 7], [0, 3], [3, 17]])
        c = Curve(numpy_array)
        assert c.x.tolist() == numpy_array[:, 0].tolist()
        assert c.y.tolist() == numpy_array[:, 1].tolist()

    def test_numpy_view_init(self):
        # todo
        pass

    def test_empty_init(self):
        with pytest.raises(TypeError):
            Curve()
        with pytest.raises(IndexError):
            Curve([])

    def test_one_point_init(self):
        c = Curve([[1, 2]])
        assert c.x == 1
        assert c.y == 2

    def test_two_point_init(self):
        c = Curve([[-1, 3], [1, 7]])
        assert c.x.tolist() == [-1, 1]
        assert c.y.tolist() == [3, 7]


class TestCurveRescale(unittest.TestCase):
    def setUp(self):
        self.pre = Curve([[0.0, 0], [5, 5], [10, 10]])
        self.post = Curve([[0.0, 0], [5, 5], [10, 10]])

    def test_rescale_by_one(self):
        self.post.rescale(factor=1)
        assert list(self.pre.x) == list(self.post.x)
        assert list(self.pre.y) == list(self.post.y)

    def test_rescale_by_negative_one(self):
        self.post.rescale(factor=-1)
        assert list(self.pre.x) == list(self.post.x)
        assert list(self.pre.y) == list(self.post.y * -1)

    def test_rescale_by_zero(self):
        # post.y should contain some nans and infs
        self.post.rescale(factor=0)
        assert list(self.pre.x) == list(self.post.x)
        assert list(self.pre.y) != list(self.post.y)
        assert str(self.post.y[0]) == 'nan'
        assert str(self.post.y[1]) == 'inf'


class TestCurveSmooth(unittest.TestCase):
    def setUp(self):
        self.pre = Curve([[0.0, 0], [5, 5], [10, 0]])
        self.post = Curve([[0.0, 0], [5, 5], [10, 0]])

    def test_smooth_with_window_one(self):
        self.post.smooth(window=1)
        assert list(self.pre.x) == list(self.post.x)
        assert list(self.pre.y) == list(self.post.y)

    def test_smooth_with_negative_window(self):
        with pytest.raises(ValueError):
            self.post.smooth(window=-1)

    def test_smooth_wtih_window_zero(self):
        with pytest.raises(ValueError):
            self.post.smooth(window=0)

    #
    # def test_y_at_x(self):
    #     self.fail()
    #
    # def test_change_domain(self):
    #     self.fail()
    #
    # def test_rebinned(self):
    #     self.fail()
    #
    # def test_evaluate_at_x(self):
    #     self.fail()
    #
    # def test_subtract(self):
    #     self.fail()
