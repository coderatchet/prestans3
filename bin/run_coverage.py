#!/bin/env/python

import os
import sys
from subprocess import Popen, PIPE, STDOUT


if __name__ == '__main__':
    if 'TRAVIS' in os.environ and os.environ.get('TRAVIS_PYTHON_VERSION', 'unknown-version') == '3.5':
        current_dir = os.path.dirname(os.path.abspath(__file__))
        setup_file = os.path.join(current_dir, os.pardir, "setup.py")
        source = os.path.join(current_dir, os.pardir, 'prestans3')
        rc = Popen(['coverage', 'run', '--source={}'.format(source),
                    setup_file, 'test'], stdout=PIPE, stderr=STDOUT)
        while True:
            line = rc.stdout.readline()
            if not line:
                break
            print(line)
        exit(rc.wait(timeout=5))
    else:
        print("skipping coverage for python version: {}".format(
            os.environ.get('TRAVIS_PYTHON_VERSION',
                           ".".join([str(v) for v in sys.version_info]))))
        raise SystemExit(0)
