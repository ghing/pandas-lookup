#!/usr/bin/env python

from setuptools import setup

install_requires = [
    'pandas',
    'requests>=2.9.1',
    'pyyaml>=3.11'
]

description = 'pandas-lookup adds remote lookup tables to a Pandas DataFrame.'

setup(
    name='pandas-lookup',
    version='0.1.0',
    description=description,
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author='Geoff Hing',
    author_email='geoffhing@gmail.com',
    url='https://github.com/ghing/pandas-lookup',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=[
        'pandaslookup'
    ],
    install_requires=install_requires
)
