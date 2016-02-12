import urllib.request
from beprof.curve import Curve
import numpy as np

url = 'http://berkeleyearth.lbl.gov/auto/Global/Complete_TAVG_complete.txt'

data = urllib.request.urlopen(url)

#skip lines with plain text
for i in range(0, 36):
    data.readline()

all = np.genfromtxt(data)

x = np.array(range(0, 1000))
y = all[:1000,3]

example = Curve(np.stack((x, y), axis=1))
print(example)

