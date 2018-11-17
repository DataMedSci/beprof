import setuptools
import sys
from pkg_resources import parse_version

def get_version():
    return None

with open('README.rst') as readme_file:
    readme = readme_file.read()

# requiring pytest-runner only when pytest is invoked
needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
pytest_runner = ['pytest-runner'] if needs_pytest else []

# set specific numpy version for python 3.2 and 3.3
numpy_version = [
    "numpy<1.12,>=1.8;python_version >= '3.2' and python_version < '3.4'",
    "numpy>=1.8;python_version < '3.0' or python_version >= '3.4'"
]

# python 3.2 doesn't understand environment markers
if sys.version_info.major == 3 and sys.version_info.minor == 2:
    numpy_version = ['numpy<1.12']

setuptools.setup(
    name='beprof',
    version=get_version(),
    packages=['beprof', 'beprof.tests'],
    test_suite='beprof.tests',
    url='https://github.com/DataMedSci/beprof',
    license='GPL',
    author='Leszek Grzanka, Mateusz Krakowski, Agnieszka Rudnicka',
    author_email='grzanka@agh.edu.pl',
    description='Beam Profile Analysing Tools',
    long_description=readme + '\n',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: Physics',

        # OS and env
        'Environment :: Console',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Unix',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=numpy_version,
    setup_requires=[] + pytest_runner,
    tests_require=['pytest']
)
