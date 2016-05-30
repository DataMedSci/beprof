from unittest import TestCase

from beprof.curve import Curve


class TestCurve(TestCase):
    def setUp(self):
        self.pre = Curve([[0.0, 0], [5, 5], [10, 0]])
        self.post = Curve([[0.0, 0], [5, 5], [10, 0]])

    def test_rescale_by_one(self):
        self.post.rescale(1)
        self.assertEqual(list(self.pre.x), list(self.post.x))
        self.assertEqual(list(self.pre.y), list(self.post.y))
    #
    # def test_smooth(self):
    #     self.fail()
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
