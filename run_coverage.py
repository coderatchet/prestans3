#!/bin/env/python

import os

from subprocess import call

if __name__ == '__main__':
    if 'TRAVIS' in os.environ and 'TRAVIS_PYTHON_VERSION' in os.environ and os.environ['TRAVIS_PYTHON_VERSION'] == '3.5':
        rc = call(['coverage', 'run', '--source=prestans3', 'python', os.path.expandvars('${toxinidir}/setup.py'), 'test'])
        raise SystemExit(rc)
