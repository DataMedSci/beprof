from beprof import profile
from beprof import curve
import numpy as np
from matplotlib import pyplot as plt
import math


class CrosswiseProfile(profile.Profile):
    def penumbra_left(self):
        return self.x_at_y(0.1, True)-self.x_at_y(0.9, True)

    def penumbra_right(self):
        return self.x_at_y(0.9)-self.x_at_y(0.1)

    def field_ratio(self, level):
        return self.width(level)/self.width(0.5)

    def symmetry(self, level):
        a = math.fabs(self.x_at_y(level, False))
        b = math.fabs(self.x_at_y(level, True))
        return (math.fabs(a-b)/(a+b)) * 200

    def flatness_50(self):
        d = (self.penumbra_left()+self.penumbra_right())/2
        left = self.x_at_y(0.5) + 2*d
        right = self.x_at_y(0.5, True) - 2*d

        p_max = np.max(self.y[np.logical_and(self.x <= right, self.x >= left)])
        p_min = np.min(self.y[np.logical_and(self.x <= right, self.x >= left)])
        
        return ((p_max-p_min)/(p_max+p_min)) * 100

    def flatness_90(self):
        d = (self.penumbra_left()+self.penumbra_right())/2
        left = self.x_at_y(0.9) + d
        right = self.x_at_y(0.9, True) - d

        p_max = np.max(self.y[np.logical_and(self.x <= right, self.x >= left)])
        p_min = np.min(self.y[np.logical_and(self.x <= right, self.x >= left)])

        return ((p_max-p_min)/(p_max+p_min)) * 100

    def asymmetry(self):
        area_left = np.trapz(self.y[self.x <= 0], self.x[self.x <= 0])
        area_right = np.trapz(self.y[self.x >= 0], self.x[self.x >= 0])

        return ((area_left - area_right)/(area_left + area_right)) * 100

    def normalize(self, dt):
        """
        Normalize to 1 over [-dt, +dt] area from the mid of the profile
        """
        a = self.y.max() - self.y.min()
        a /= 2
        w = self.width(a)
        mid = self.x_at_y(a) + w/2
        self.x -= mid
        
        ave = np.average(self.y[np.fabs(self.x) <= dt])

        self.y /= ave

    def absolute_y(self):
        self.y = self.y - self.y.min()

    def draw(self):
        plt.title("Crosswise Profile")
        plt.xlabel("X")
        plt.ylabel("E8/E7")
        plt.plot(self.x,self.y)
        plt.show()
