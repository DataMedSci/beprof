import urllib.request
from beprof.curve import Curve
import numpy as np

url = 'http://berkeleyearth.lbl.gov/auto/Global/Complete_TAVG_complete.txt'

y = np.genfromtxt(urllib.request.urlopen(url), skip_header=35, skip_footer=2192, usecols=3)
x = np.arange(0, 1000)

example = Curve(np.stack((x, y), axis=1))
print(example)
