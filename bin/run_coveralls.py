#!/bin/env/python
# -*- coding: utf-8 -*-
"""
    run_coveralls.py
    ~~~~~~~~~~~~~~~~

    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""

import os
import sys
from subprocess import Popen, STDOUT, PIPE

if __name__ == '__main__':
    if 'TRAVIS' in os.environ:
        coverage_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, '.coveragerc')
        rc = Popen(['coveralls'], stdout=PIPE, stderr=STDOUT)
        while True:
            line = rc.stdout.readline()
            if not line:
                break
            print(line)
        if sys.version_info.major == 2:
            exit(rc.wait())
        else:
            exit(rc.wait(timeout=5))
    else:
        print("skipping coverage for python version: {}".format(
            os.environ.get('TRAVIS_PYTHON_VERSION',
                           ".".join([str(v) for v in sys.version_info]))))
        raise SystemExit(0)
