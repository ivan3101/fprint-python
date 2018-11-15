#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""CFFI bindings for libfprint"""

import os
from distutils.core import setup, Extension

setup(
    name="pyfprint-cffi",
    version="0.1",
    description="CFFI bindings for libfprint",
    author="Francisco Demartino",
    author_email="demartino.francisco@gmail.com",
    url="https://github.com/franciscod/pyfprint-cffi",
    license="GPL-2",
    packages=["pyfprint"],
    install_requires=[
        "cffi==0.8.6",
        "Pillow",
    ],
)
