#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import taggit_serializer

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = taggit_serializer.__version__

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()


setup(
    name='django-taggit-serializer',
    version=version,
    description="""The Django Taggit serializer for tDjango REST Framework""",
    long_description="The Django Taggit Serializer for the Django"
                     "REST Framework developers. "
                     "Installation can be found on "
                     "https://github.com/glemmaPaul/django-taggit-serializer",
    author='Paul Oostenrijk',
    author_email='paul@glemma.nl',
    url='https://github.com/glemmaPaul/django-taggit-serializer',
    packages=[
        'taggit_serializer',
    ],
    include_package_data=True,
    install_requires=[
        'django-taggit',
    ],
    license="BSD",
    zip_safe=False,
    keywords='django-taggit-serializer',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
)