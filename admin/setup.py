#!/usr/bin/env python

license = open('UNLICENSE').read()
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

long_description = open('README.md').read()

setup(
    name="fred",
    version="1.3",
    description="St. Louis Federal Reserve FRED API",
    long_description=long_description,
    keywords="fred, fred api, federal reserve, st. louis fed",
    author="Zach Williams",
    author_email="hey@zachwill.com",
    url="https://github.com/zachwill/fred",
    license="Unlicense (a.k.a. Public Domain)",
    packages=["fred"],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Topic :: Internet',
        'Topic :: Internet :: WWW/HTTP',
        ],
    test_suite="test.py",
    tests_require=["mock", "Mock"]
    )
