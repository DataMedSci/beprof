import setuptools
from pkg_resources import parse_version
try:
    import versioneer
except ImportError:
    # dirty hack needed by readthedoc generation tool
    import subprocess
    subprocess.call(["versioneer", "install"])
    import versioneer

version = versioneer.get_version()
parsed_version = parse_version(version)
if '*@' in parsed_version[1]:
    import time
    version += str(int(time.time()))


packages = ['beprof']

with open('README.rst') as readme_file:
    readme = readme_file.read()

setuptools.setup(
    name='beprof',
    version=version,
    packages=packages,
    url='https://github.com/DataMedSci/beprof',
    license='GPL',
    author=['Leszek Grzanka','Mateusz Krakowski', 'ant6'],
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
        'Topic :: Software Development :: Build Tools',

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
    install_requires=[
        'numpy>=1.10.4',
        'scipy>=0.16.0',
    ],
    cmdclass=versioneer.get_cmdclass(),

)
