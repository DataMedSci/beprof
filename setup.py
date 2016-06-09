import setuptools
from pkg_resources import parse_version


def pip_command_output(pip_args):
    import sys
    import pip
    from io import StringIO
    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()
    pip.main(pip_args)
    output = mystdout.getvalue()
    mystdout.truncate(0)
    sys.stdout = old_stdout
    print("result", pip_args, len(output), output)
    return output


try:
    # assume versioneer.py was generated using "versioneer install" command
    import versioneer
except ImportError:
    # it looks versioneer.py is missing
    # lets assume that versioneer package is installed
    # and versioneer binary is present in $PATH
    import subprocess
    try:
        # call versioneer install to generate versioneer.py
        subprocess.call(["versioneer", "install"])
    except IOError:
        # it looks versioneer is missing from $PATH
        # probably versioneer is installed in some user directory

        # query pip for list of files in versioneer package
        output = pip_command_output(["show", "-f", "versioneer"])

        # now we parse the results
        main_path = [x[len("Location: "):] for x in output.split('\n')
                     if x.startswith("Location")][0]
        bin_path = [x[len("  "):] for x in output.split('\n')
                    if x.endswith("/versioneer")][0]

        # exe_path is absolute path to versioneer binary
        import os
        exe_path = os.path.join(main_path, bin_path)
        # call versioneer install to generate versioneer.py
        subprocess.call([exe_path, "install"])

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
    author=['Leszek Grzanka', 'Mateusz Krakowski', 'ant6'],
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
