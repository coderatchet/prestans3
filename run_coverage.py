#!/bin/env/python

import os
import sys
from subprocess import Popen, PIPE, STDOUT

if __name__ == '__main__':
    if 'TRAVIS' in os.environ and os.environ.get('TRAVIS_PYTHON_VERSION', 'unknown-version') == '3.5':
        rc = Popen(['coverage', 'run', '--source=prestans3', '--rcfile', os.path.expandvars('${envdir}/.coveragerc'), 'python', os.path.expandvars('${toxinidir}/setup.py'), 'test'], stdout=PIPE, stderr=STDOUT)
        while True:
            line = rc.stdout.readline()
            if not line:
                break
            print(line)
        raise SystemExit(rc)
    else:
        print("skipping coverage for python version: {}",
              os.environ.get('TRAVIS_PYTHON_VERSION',
                             ".".join([str(v) for v in sys.version_info])))
        raise SystemExit(0)
