from curve import Curve, DataSerie
from profile import Profile, LateralProfile
import numpy as np
import unittest

cur = Curve([[0, 0], [1, 1], [2, 2], [3, 2], [4, 3], [5, 4], [6, 4], [7, 3], [8, 2], [9, 1], [10, 0]],
            arg1 = 'first',
            arg2 = 'second'
            )
pro = Profile([[0, 0], [1, 2]])
lpr = LateralProfile([[0, 0], [1, 2]])


class TestCurveMethods(unittest.TestCase):

    def test_metadata_1(self):
        # check if everything was OK with constructing object with metadata
        self.assertEqual(cur.metadata['arg1'], 'first')
        self.assertEqual(cur.metadata['arg2'], 'second')
        # check if object after change_domain still has metadata
        obj = cur.change_domain([0, 1, 2.5, 5])
        self.assertEqual(obj.metadata['arg1'], 'first')
        self.assertEqual(obj.metadata['arg2'], 'second')
        # try creating new obj with slicing and check metadata
        obj = cur[2:5]
        self.assertEqual(obj.metadata['arg1'], 'first')
        self.assertEqual(obj.metadata['arg2'], 'second')

    def test_y_at_x(self):
        # return value of X from domain
        self.assertEqual(cur.y_at_x(0), 0)
        # return value of X not in domain (but in domains range)
        self.assertEqual(cur.y_at_x(2.5), 2)
        # X out of domain range - should return nan
        self.assertTrue(np.isnan(cur.y_at_x(-1)))

    def test_change_domain(self):
        # new domain inside current domain
        self.assertEqual(list(cur.change_domain([2, 3, 4]).x), [2, 3 ,4])
        self.assertEqual(list(cur.change_domain([2, 3, 4]).y), [2, 2 ,3])

        # new domain's range not inside current
        self.assertEqual(list(cur.change_domain([-1, 4]).x), list(cur.x))
        self.assertEqual(list(cur.change_domain([0, 11]).x), list(cur.x))

    def test_rebinned(self):
        # different combinations
        self.assertEqual(list(cur.rebinned(step=1, fixp=0.5).x),
                         [0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5]
                         )

if __name__ == '__main__':
    unittest.main()
