# beprof
Beam Profile Analysing Tools

Library provides methods to work with Beam Profiles which are sets of points <br>
(might be 2-D or 3-D also with extra metadata) sorted by one of coordinates.

beprof is based on nparray class from numpy, and it provides <br>
numerous tools for different computations and data analysis.

# installation

Current version (0.1.0) is not available on PyPi, although once a <br>
stable version is ready it will be pushed to PyPi repo.<br><br>

For now, installation can be done from this GIT repository, using <br>
`~$ pip3 install git+https://github.com/grzanka/beprof.git@master` <br>

(where `@master` refers to the name of a branch)

To unistall, simply use:<br>

`~$ pip3 uninstall beprof`<br>


# usage

Once you install beprof, you should be able to import is as a python module<br>
Using ipython the code would be i.e.<br>
```
import beprof
from beprof import curve  #imports curve module
from beprof import profile  #imports profile module
```

Once you import necessery modules, you can use them to work with i.e. profiles:<br>

```
from beprof import profile
dir(profile)
p = profile.Profile([[0, 1], [1, -1], [2, 3], [4, 0]])
print(p)
```

A few examples of data you can work with using beprof can be downloaded from<br>
another branch of this project named `feature/examples`
https://github.com/grzanka/beprof.git
<br>

You can also use another modules as numpy or matplotlib to work with beprof:
```
#assuming you already defined p as above
import numpy as np
import matplotlib.pyplot as plt
foo = np.asarray(p)
print(foo.shape())
plt.plot(foo[:,0], foo[:,1])
plt.show()
```

