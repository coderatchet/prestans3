#!/bin/env/python
# -*- coding: utf-8 -*-
"""
    run_coverage.py
    ~~~~~~~~~~~~~~~

    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""
import os
import sys
from subprocess import Popen, PIPE, STDOUT
from future.utils import PYPY, PY2, PY3, PY27

print("PYPY: {}".format(PYPY))
print("PY2: {}".format(PY2))
print("PY27: {}".format(PY27))
print("PY3: {}".format(PY3))

if __name__ == '__main__':
    if 'TRAVIS' in os.environ:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        setup_file = os.path.join(current_dir, os.pardir, "setup.py")
        source = os.path.join(current_dir, os.pardir, 'prestans3')
        future_source = os.path.join(current_dir, os.pardir, 'prestans3', 'future', '*')
        rc = Popen(['coverage', 'run', '--source={}'.format(source), '--omit={}'.format(future_source),
                    setup_file, 'test'], stdout=PIPE, stderr=STDOUT)
        while True:
            line = rc.stdout.readline()
            if not line:
                break
            # py2to3 execute only else statement
            if sys.version_info.major == 2:
                sys.stdout.write(str(line))
            else:
                sys.stdout.write(line.decode('utf-8'))
            sys.stdout.flush()
        # py2to3 execute only else statement
        if sys.version_info.major == 2:
            exit(rc.wait())
        else:
            # noinspection PyArgumentList
            exit(rc.wait(timeout=5))
    else:
        print("skipping coverage for python version: {}".format(
            os.environ.get('TRAVIS_PYTHON_VERSION',
                           ".".join([str(v) for v in sys.version_info]))))
        raise SystemExit(0)
