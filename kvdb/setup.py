#!/usr/bin/env python

from setuptools import setup


setup(
    name='kvdb',
    version='2',
    url='https://github.com/rcbensley/mariadb-dba/kvdb',
    description='Key-Value-Database',
    packages=['kvdb'],
    install_requires=['pymysql', ],
    keywords='kvdb',
)
