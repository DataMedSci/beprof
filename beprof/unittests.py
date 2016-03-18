from curve import Curve, DataSerie
from profile import Profile, LateralProfile
import numpy as np

cur = Curve([[0, 0], [1, 1], [2, 2], [3, 2], [4, 3], [5, 4], [6, 4], [7, 3], [8, 2], [9, 1], [10, 0]],
        arg1 = 'first',
        arg2 = 'second'
        )
pro = Profile([[0, 0], [1, 1], [2, 2], [3, 2], [4, 3], [5, 4], [6, 4], [7, 3], [8, 2], [9, 1], [10, 0]],
        profile1 = 'first_prof',
        profile2 = 'second_prof'
        )

def main():

    if cur.y_at_x(0) == 0:
        print('-'*10, 'PASSED', '-'*10)
    else:
        print('X'*10, 'FAILED', 'X'*10)

    if cur.y_at_x(2.5) == 2:
        print('-'*10, 'PASSED', '-'*10)
    else:
        print('X'*10, 'FAILED', 'X'*10)

    if np.array_equal(cur.change_domain([2, 3, 4]).x, [2, 3 ,4]):
        print('-'*10, 'PASSED', '-'*10)
    else:
        print('X'*10, 'FAILED', 'X'*10)


    if pro.x_at_y(1) == 1:
        print('-'*10, 'PASSED', '-'*10)
    else:
        print('X'*10, 'FAILED', 'X'*10)

    if cur.metadata['arg1'] == 'first':
        print('-'*10, 'PASSED', '-'*10)
    else:
        print('X'*10, 'FAILED', 'X'*10)

    if pro.metadata['profile2'] == 'second_prof':
        print('-'*10, 'PASSED', '-'*10)
    else:
        print('X'*10, 'FAILED', 'X'*10)

if __name__=='__main__':
    main()
