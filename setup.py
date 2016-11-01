#!/usr/bin/env python

from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md')) as f:
    description = f.read()

setup(
    name='cinch',
    version='0.1.6',
    description='Cinch continuous integration setup',
    long_description=description,
    url='https://github.com/RedHatQE/cinch',
    author='RedHatQE',
    license='GPLv3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: QE, Administrators',
        'Topic :: Software Development :: Continuous Integration',
        'Licenese :: OSI Approved :: GPL Version 3',
        'Programming Language :: Python :: 2.7'
    ],
    keywords='continuous integration, ci, jenkins',
    packages=find_packages(exclude=('library', 'bin')),
    include_package_data=True,
    install_requires=[
        'ansible==2.1.*'
    ],
    entry_points={
        'console_scripts': [
            'cinch=cinch.bin.entry_point:cinch'
        ]
    }
)
