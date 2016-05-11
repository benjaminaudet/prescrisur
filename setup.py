#!/usr/bin/env python

from setuptools import setup

setup(name='prescrisur',
      version='1.0',
      description='Prescrisur app',
      author='Pierrick BOUTRUCHE',
      packages=[
          'api',
          'api/models',
          'api/update',
          'front'
      ],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'Flask',
          'Flask-Login',
          'pymongo',
          'jsonpickle',
          'bleach',
          'passlib'
      ]
      )
