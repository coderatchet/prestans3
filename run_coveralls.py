#!/bin/env/python

import os
import sys
from subprocess import Popen, PIPE, STDOUT

if __name__ == '__main__':
    if 'TRAVIS' in os.environ and 'TRAVIS_PYTHON_VERSION' in os.environ and os.environ['TRAVIS_PYTHON_VERSION'] == '3.5':
        rc = Popen(['coveralls', '--rcfile', os.path.expandvars('${envdir}/.coveragerc')], stdout=PIPE, stderr=STDOUT)
        while True:
            line = rc.stdout.readline()
            if not line:
                break
            print(line)
        raise SystemExit(rc)
    else:
        print("skipping coverage for python version: {}",
              os.environ.get('TRAVIS_PYTHON_VERSION',
                             ".".join(sys.version_info)))
        raise SystemExit(0)
