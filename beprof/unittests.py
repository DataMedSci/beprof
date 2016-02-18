from beprof.curve import Curve, DataSerie
from beprof.profile import Profile, LateralProfile
import numpy as np
import unittest
import copy

cur = Curve([[0, 0], [1, 1], [2, 2], [3, 2], [4, 3], [5, 4], [6, 4], [7, 3], [8, 2], [9, 1], [10, 0]],
            arg1 = 'first',
            arg2 = 'second'
            )
pro = Profile([[0, 0], [1, 1], [2, 2], [3, 2], [4, 3], [5, 4], [6, 4], [7, 3], [8, 2], [9, 1], [10, 0]],
            profile1 = 'first_prof',
            profile2 = 'second_prof'
            )
lpr = LateralProfile([[0, 0], [1, 1], [2, 2], [3, 2], [4, 3], [5, 4], [6, 4], [7, 3], [8, 2], [9, 1], [10, 0]],
            lprof1 = 'first_lp',
            lprof2 = 'second_lp'
            )


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
class TestProfileMethods(unittest.TestCase):

    def test_metadata_1(self):
        # check if everything was OK with constructing object with metadata
        self.assertEqual(pro.metadata['profile1'], 'first_prof')
        self.assertEqual(pro.metadata['profile2'], 'second_prof')
        # check if object after change_domain still has metadata
        obj = pro.change_domain([0, 1, 2.5, 5])
        self.assertEqual(obj.metadata['profile1'], 'first_prof')
        self.assertEqual(obj.metadata['profile2'], 'second_prof')
        # try creating new obj with slicing and check metadata
        obj = pro[2:5]
        self.assertEqual(obj.metadata['profile1'], 'first_prof')
        self.assertEqual(obj.metadata['profile2'], 'second_prof')
        # try get non existing metadata
        with self.assertRaises(KeyError):
            pro.metadata['example']
            obj.metadata['non-existing']

    def test_x_at_y(self):
        self.assertEqual(pro.x_at_y(1), 1)
        self.assertEqual(pro.x_at_y(1, reverse=True), 9)

        # y value out of range
        self.assertTrue(np.isnan(pro.x_at_y(5)))

    def test_mirror(self):
        # mirroring twice should be like non mirroring at all
        orgx = copy.deepcopy(lpr.x)
        orgy = copy.deepcopy(lpr.y)
        lpr.mirror()
        lpr.mirror()
        self.assertEqual(list(lpr.x), list(orgx))
        self.assertEqual(list(lpr.y), list(orgy))
        # simple example
        lpr.mirror(m=4)
        self.assertEqual(list(lpr.y), list(orgy[::-1]))

class TestTypes(unittest.TestCase):

    # testing different combinations of profiles using curve methods
    # check whether type of returned object and metadata is OK
    # need more up-to-date version of repo, all tests will fail on this level
    def test_rebinning(self):
        # todo
        pass

    def test_change_domain(self):
        # todo
        pass

class TestExceptions(unittest.TestCase):
    def test_exceptions(self):
        # todo
        pass

if __name__ == '__main__':
    unittest.main()
