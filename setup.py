from setuptools import setup, find_packages
import sys

sys.path.append("./src")

import autest


setup(name="autest",
        version=autest.__version__,
        description="Resuable gold file testing system",
        long_description='''Resuable Gold testing system, or autest for short, is a testing system targeted toward gold file, command line process testing.

Goals
----------------------------------

* Easy to write and add tests
* Extensible system to allow: 
 * Adding new functionality for testing your application
 * Batch commands as a new function to make it easier to write tests
 * Define custom report outputs
* Percise as possible error messages to make it easy to see what is wrong fast
* Sandbox to make it easy to see what failed and reproduce out of test system
* Flexibale gold file synatx to make it easier to ignore text that is not important
* Run on python 2 or 3

Non-Goals
----------------------------------

The Resuable Gold testing system is not about making another unit testing framework.
        ''',
        author="Jason Kenny",
        author_email="dragon512@live.com",
        url="https://bitbucket.org/dragon512/reusable-gold-testing-system",
        license="MIT",
        package_dir = {'': 'src'},
        packages=find_packages('src',exclude=('test')),
        entry_points={
          'console_scripts': ['autest = autest.__main__:main']
          },
        install_requires =[
                "colorama",
                "future",
                "psutil"
                ],

        package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt'],
        
        },

        # see classifiers
        # http://pypi.python.org/pypi?%3Aaction=list_classifiers
         classifiers=[
            'Development Status :: 5 - Production/Stable', 
            'Environment :: Console', 
            'Intended Audience :: Developers', 
            'License :: OSI Approved :: MIT License', 
            'Operating System :: OS Independent', 
            'Programming Language :: Python :: 2', 
            'Programming Language :: Python :: 2.7', 
            'Programming Language :: Python :: 3', 
            'Programming Language :: Python :: 3.4', 
            'Programming Language :: Python :: 3.5', 
            'Topic :: Terminals',
            ],
)
