#!/usr/bin/env python
import os
import shutil
from setuptools import setup, find_packages

CUR_PATH = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(CUR_PATH, "build")
if os.path.isdir(path):
    print("INFO DEL DIR ", path)
    shutil.rmtree(path)
path = os.path.join(CUR_PATH, "dist")
if os.path.isdir(path):
    print("INFO DEL DIR ", path)
    shutil.rmtree(path)

info = {}
with open(os.path.join(CUR_PATH, "meo/__version__.py"), 'r+', encoding='utf8') as f:
    exec(f.read(), info)

with open(os.path.join(CUR_PATH, "description.md"), 'r+', encoding='utf8') as f:
    long_description = f.read()

setup(
    name         =  info['__title__'],
    author       =  info["__author__"],
    url          =  info["__url__"],
    description  =  info["__description__"],
    version      =  '.'.join(map(str, info["__version__"])),
    license      =  info["__license__"],
    author_email =  info["__author_email__"],
    packages     = find_packages(),
    include_package_data = True,
    long_description     = long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'json5>=0.9',
        'pyzipper>=0.3.6'
    ],
)
