#!/usr/bin/env bash

set -x # Print command traces before executing command

set -e # Exit immediately if a simple command exits with a non-zero status.

set -o pipefail # Return value of a pipeline as the value of the last command to
                # exit with a non-zero status, or zero if all commands in the
                # pipeline exit successfully.

# file inspired by https://github.com/pyca/cryptography

# MacOSX hav Python 2.7 installed by default, lets use it. We just need to install pip
if [[ $TOXENV == py27* ]] ;
then
    curl -O https://bootstrap.pypa.io/get-pip.py
    python get-pip.py --user
    pip install --user --upgrade pip
    pip install --user --upgrade virtualenv
    pip install --user --upgrade tox
    exit 0
fi

# At this point we run default Python 2.7 interpreter
# versioneer doesn't support Python 3.2, so we run it now with current interpreter
# for other interpreters pointed out by TOXENV look at the end of the script
if [[ $TOXENV == py32* ]] ;
then
    pip install --user --upgrade versioneer
    $HOME/Library/Python/2.7/bin/versioneer install
fi

# For Python 3, first install pyenv
brew update || brew update
brew unlink pyenv && brew install pyenv && brew link pyenv

# Also git will be needed later
brew unlink git && brew install git && brew link git

# setup pyenv
PYENV_ROOT="$HOME/.pyenv"
PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"

# install Python 3.x
case "${TOXENV}" in
        py32*)
            pyenv install 3.2
            pyenv global 3.2
            ;;
        py33*)
            pyenv install 3.3.6
            pyenv global 3.3.6
            ;;
        py34*)
            pyenv install 3.4.4
            pyenv global 3.4.4
            ;;
        py35*)
            pyenv install 3.5.1
            pyenv global 3.5.1
            ;;
        py36*)
            pyenv install 3.6-dev
            pyenv global 3.6-dev
            ;;
        *)
        exit 1
esac

pyenv rehash

# install virtualenv and tox ($VENVVER and $PIPVER is set only for python 3.2)
pyenv exec pip install --upgrade virtualenv$VENVVER pip$PIPVER tox

# versioneer doesn't support Python 3.2, if TOXENV=py32 versioneer was set up at the begining of the script
# for other interpreters we run it here with such interpreter as TOXENV points out
if [[ $TOXENV != py32* ]] ;
then
    pyenv exec pip install --upgrade versioneer
    pyenv exec versioneer install
fi