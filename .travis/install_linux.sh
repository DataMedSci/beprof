#!/usr/bin/env bash

set -x # Print command traces before executing command

set -e # Exit immediately if a simple command exits with a non-zero status.

set -o pipefail # Return value of a pipeline as the value of the last command to
                # exit with a non-zero status, or zero if all commands in the
                # pipeline exit successfully.

# check ubuntu version
lsb_release -a

pip install --upgrade virtualenv$VENVVER pip$PIPVER setuptools tox

pip install --upgrade versioneer

versioneer install