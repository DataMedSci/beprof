===============================
beprof
===============================

.. image:: https://img.shields.io/pypi/v/beprof.svg
        :target: https://pypi.python.org/pypi/beprof

.. image:: https://img.shields.io/travis/DataMedSci/beprof.svg
        :target: https://travis-ci.org/DataMedSci/beprof

.. image:: https://readthedocs.org/projects/beprof/badge/?version=latest
        :target: https://readthedocs.org/projects/beprof/?badge=latest
        :alt: Documentation Status

========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - |travis| |appveyor| |requires| |codeclimate|
    * - package
      - |version| |downloads| |wheel| |supported-versions| |supported-implementations|

.. |docs| image:: https://readthedocs.org/projects/beprof/badge/?style=flat
    :target: https://readthedocs.org/projects/beprof
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/DataMedSci/beprof.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/DataMedSci/beprof

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/y06jw47ir3gvvgta?svg=true
    :alt: Appveyor Build Status
    :target: https://ci.appveyor.com/project/grzanka/beprof

.. |requires| image:: https://requires.io/github/DataMedSci/beprof/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/DataMedSci/beprof/requirements/?branch=master

.. |codeclimate| image:: https://codeclimate.com/github/DataMedSci/beprof/badges/issue_count.svg
    :target: https://codeclimate.com/github/DataMedSci/beprof
    :alt: Issue Count

.. |version| image:: https://img.shields.io/pypi/v/beprof.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/beprof

.. |downloads| image:: https://img.shields.io/pypi/dm/beprof.svg?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/beprof

.. |wheel| image:: https://img.shields.io/pypi/wheel/beprof.svg?style=flat
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/beprof

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/beprof.svg?style=flat
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/beprof

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/beprof.svg?style=flat
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/beprof

.. end-badges

Overv.io issue board: https://overv.io/DataMedSci/beprof/

Beam Profile Analysing Tools

Library provides methods to work with Beam Profiles which are sets of points
(2-D with optional metadata) sorted by one of coordinates.
cd
beprof is based on nparray class from numpy, and it provides
numerous tools for different computations and data analysis.

Installation
============

Current version available on testing PyPi server, although once a
stable version is ready it will be pushed to official PyPi repo.

For now, installation can be done from this GIT repository, using::

    pip install setuptools versioneer
    pip install git+https://github.com/DataMedSci/beprof.git

To unistall, simply use::

    pip uninstall beprof

Documentation
=============

https://beprof.readthedocs.io/

Features
--------

Once you install beprof, you should be able to import is as a python module
Using ipython the code would be i.e.::

    import beprof
    from beprof import curve  #imports curve module
    from beprof import profile  #imports profile module

Once you import necessary modules, you can use them to work with i.e. profiles::

    from beprof import profile
    dir(profile)
    p = profile.Profile([[0, 1], [1, -1], [2, 3], [4, 0]])
    print(p)

You can also use another modules as numpy or matplotlib to work with beprof::

    #assuming you already defined p as above
    import numpy as np
    import matplotlib.pyplot as plt
    foo = np.asarray(p)
    print(foo.shape())
    plt.plot(foo[:,0], foo[:,1])
    plt.show()


Note that beprof is a library and end-users shouldn't "run it".
It is also strongly discouraged to use *git clone* to download code.
Git is only for developers, end-users should use pip installation.
If you are interested in development - have a look at CONTRIBUTING_ section.

.. _CONTRIBUTING: https://github.com/DataMedSci/beprof/blob/master/CONTRIBUTING.rst

Credits
---------

This package was created with Cookiecutter_ and the `grzanka/cookiecutter-pip-docker-versioneer`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`grzanka/cookiecutter-pip-docker-versioneer`: https://github.com/grzanka/cookiecutter-pip-docker-versioneer
