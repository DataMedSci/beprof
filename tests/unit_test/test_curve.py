import pytest
import unittest
from beprof.curve import Curve


class TestCurve(unittest.TestCase):
    def setUp(self):
        self.pre = Curve([[0.0, 0], [5, 5], [10, 0]])
        self.post = Curve([[0.0, 0], [5, 5], [10, 0]])

    # TEST RESCALE
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

    # TEST SMOOTH
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
