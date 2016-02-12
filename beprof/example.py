import urllib.request
from beprof.curve import Curve
import numpy as np

url = 'http://berkeleyearth.lbl.gov/auto/Global/Complete_TAVG_complete.txt'
data = urllib.request.urlopen(url)

all = np.genfromtxt(data, skip_header=35, skip_footer=2192)
print(np.shape(all))
x = np.array(range(0, 1000))
y = all[:,3]

example = Curve(np.stack((x, y), axis=1))
print(example)

