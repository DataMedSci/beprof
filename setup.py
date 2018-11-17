import setuptools
import sys
import os
import subprocess
from pkg_resources import parse_version

# Return the git revision as a string
def git_version():
    def _minimal_ext_cmd(cmd):
        # construct minimal environment
        env = {}
        for k in ['SYSTEMROOT', 'PATH', 'HOME']:
            v = os.environ.get(k)
            if v is not None:
                env[k] = v
        # LANGUAGE is used on win32
        env['LANGUAGE'] = 'C'
        env['LANG'] = 'C'
        env['LC_ALL'] = 'C'
        out = subprocess.Popen(cmd, stdout=subprocess.PIPE, env=env).communicate()[0]
        return out

    try:
        out = _minimal_ext_cmd(['git', 'describe', '--tags', '--long'])
        GIT_REVISION = out.strip().decode('ascii')
        print('GIT_REVISION', GIT_REVISION)
        if GIT_REVISION:
            no_of_commits_since_last_tag = int(GIT_REVISION.split('-')[1])
            tag_name = GIT_REVISION.split('-')[0][1:]
            if no_of_commits_since_last_tag==0:
                version = tag_name
            else:
                version = '{}+rev{}'.format(tag_name, no_of_commits_since_last_tag)
        else:
            version = "Unknown"
    except OSError:
        version = "Unknown"

    return version


def write_version_py(filename='beprof/__init__.py'):
    cnt = """
__version__ = '%(version)s'
"""

    GIT_REVISION = git_version()
    VERSION=GIT_REVISION[1:]

    a = open(filename, 'a')
    try:
        a.write(cnt % {'version': GIT_REVISION})
    finally:
        a.close()

write_version_py()

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
    version=git_version(),
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
