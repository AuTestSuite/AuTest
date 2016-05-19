from setuptools import setup, find_packages
import os

print find_packages(exclude=('test'))

setup(name="autest",
        description="Resuable gold file testing system",
        author="Jason Kenny",
        author_email="dragon512@live.com",
        version="1.0.0",
        packages=find_packages(exclude=('test')),
		entry_points={
          'console_scripts': ['autest = autest.__main__:main']
          },
        install_requires =[
                "colorama",
                "future"
            ],
        #data_files = [("", ["license.txt"])],
        url="https://bitbucket.org/dragon512/reusable-gold-testing-system",
        license="MIT")
