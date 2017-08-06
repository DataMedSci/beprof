from beprof import profile
from beprof import curve
import numpy as np
from matplotlib import pyplot as plt


class CrosswiseProfile(profile.Profile):
    def penumbra(self, reverse=False):
        if reverse:
            return self.x_at_y(0.9)-self.x_at_y(0.1)
        else:
            return self.x_at_y(0.1, True)-self.x_at_y(0.9, True)

    def normalize(self, dt):
        """
        Normalize to 1 over [-dt, +dt] area from the mid of the profile
        """
        a = self.y.max() - self.y.min()
        a = a/2
        w = self.width(a)
        mid = self.x_at_y(a) + w/2
        
        ave = np.average(self.y[np.fabs(self.x - mid) <= dt])

        self.y = self.y / ave

    def absolute_y(self):
        self.y = self.y - self.y.min()

    def draw(self):
        plt.title("Crosswise Profile")
        plt.xlabel("X")
        plt.ylabel("E8/E7")
        plt.plot(self.x,self.y)
        plt.show()
