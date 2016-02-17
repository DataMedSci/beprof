# beprof setup.py

from distutils.core import setup

setup(
    name = 'beprof',
    packages = ['beprof'],
    version = '0.1.0',
    description = 'Beam profile analysing tool',
    author = ['Leszek Grzanka', 'Mateusz Krakowski'],
    author_email = 'grzanka@agh.edu.pl',
    url = 'https://github.com/grzanka/beprof',
    keywords = ["beam", "profile"],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ]
    # install_requires = [
    #     'numpy>=1.10.4', 
    #     'scipy>=0.16.0',
    #     ]
)
