# -*- coding: utf-8 -*-
"""
    setup.py
    ~~~~~~~~
    
    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""

import os
import shutil

from setuptools import setup, find_packages
from setuptools.command.install import install

from prestans3 import __version__


setup(name="prestans3")
