#!/usr/bin/env python

from setuptools import setup


setup(
    name='kvdb',
    version='0.0.1',
    url='https://github.com/rcbensley/mariadb-dba/kvdb',
    description=';)',
    packages=['kv'],
    install_requires=['pymysql', ],
    keywords='kvdb',
)
