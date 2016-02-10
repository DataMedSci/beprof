import beprof.curve
import beprof.profile
import numpy as np

def subtract(curve1, curve2, defval=0):
    '''
    Function calculates difference between curve1 and curve2 and returns new object
    which domain is an union of domains of curve1 and curve2

    :param curve1: first curve to calculate the difference
    :param curve2: second curve to calculate the difference
    :param defval: default value for points that cannot be interpolated
    :return: new curve object with element-wise difference (using interpolation if necessary)
    '''
    # domain1 = [a1, b1]
    # domain2 = [a2, b2]
    # a1, b1 = np.min(curve1.x), np.max(curve1.x)
    # a2, b2 = np.min(curve2.x), np.max(curve2.x)
    #
    # # mutual position of the domains can be 1 of 3 cases:
    # # CASE 1: domains are disjoint:
    # if a2 > b1 or a1 > b2:
    #     tmp1 = np.array(curve1.y) - defval        # new values for self.x are correspoding self.y-defval
    #     tmp2 = defval - np.array(curve2.y)          # new values for c2.x are corresponding defval - c2.y
    #     if a2 > b1:     # here we have ------a1||||||b1-----a2|||||b2------>
    #         newX = np.concatenate((curve1.x, curve2.x))        # new X is just an union
    #         newY = np.concatenate((tmp1, tmp2))    # into one list
    #     else:           # mirrored, just a minor change
    #         newX = np.concatenate((curve2.x, curve1.x))        # new X is just an union
    #         newY = np.concatenate((tmp2, tmp1))             # into one list
    #
    #     print('newX: ', newX)
    #     print('newY: ', newY)
    #     obj = curve.Curve(np.stack((newX, newY), axis=1))  # ADD METADATA HANDLING!
    #     return obj
    # # CASE 2: one domain includes the other, in this example domain(curve2) is inside domain(curve1)
    # elif a1 <= a2 and b1 >= b2:

    newX = np.union1d(curve1.x, curve2.x)
    print('newX: ', newX)
    y1 = curve1.evaluate_at_x(newX, defval)
    y2 = curve2.evaluate_at_x(newX, defval)
    newY = y1 - y2
    obj = curve.Curve(np.stack((newX, newY), axis=1))  # ADD METADATA HANDLING!
    return obj
