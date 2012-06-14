#!/usr/bin/python

from setuptools import setup

setup(name='python-nagext',
    version='0.2',
    description='Python interface to Nagios external commands',
    long_description='This module allows sending external commands to Nagios from Python',
    license='LGPL3',
    author='Alexander Duryagin',
    author_email='daa@vologda.ru',
    url='http://github.com/yshh/nagext',
    install_requires=[
        'Flask>=0.8',
        'lxml>=2.3.4',
        'requests>=0.13.1',
        ],
#    entry_points={
#        'console_scripts': ['nagext_api = nagext.api:main'],
#        },
    packages=['nagext'])
