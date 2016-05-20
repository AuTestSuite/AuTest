from setuptools import setup, find_packages
import os

setup(name="autest",
        version="1.0.0b0",
        description="Resuable gold file testing system",
        long_description="fill in",
        author="Jason Kenny",
        author_email="dragon512@live.com",
        url="https://bitbucket.org/dragon512/reusable-gold-testing-system",
        license="MIT",
        package_dir = {'': 'src'},
        packages=find_packages('src',exclude=('test')),
		entry_points={
          'console_scripts': ['autest = autest.__main__:main']
          },
        install_requires =["colorama",
                "future"],

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
