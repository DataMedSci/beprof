# beprof setup.py

from distutils.core import setup

setup(
    name = 'beprof',
    packages = ['beprof'],
    version = '1.0',
    description = 'Beam profile analysing tool',
    author = 'Mateusz Krakowski',
    author_email = 'mkrakowski.agh@gmail.com',
    url = 'https://github.com/grzanka/beprof',
    keywords = ["beam", "profile"],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ]
)
