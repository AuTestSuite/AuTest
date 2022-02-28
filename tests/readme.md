Setting up Testing
##################

Testing is generally done via nox. There is a noxfile.py defined in the root dictory to drive the testing cases.
To setup the enviroment to run against all different versions of python it is currently recommended to use `pyenv`.
Setup instructions can be found at https://github.com/pyenv/pyenv. Once installed the current setup is to install versions:


* 3.6.15
* 3.7.12
* 3.8.12
* 3.9.10
* 3.10.2
* pyston-2.3.2

These versions can then be be defined by the pyenv shim via running:

`pyenv global 3.10.2 3.6.15 3.7.12 3.8.12 3.9.10 pyston-2.3.2`

Then making sure nox is installed via: `pip install nox`

At this point running `nox` in the root directory should test AuTest against all version of python.

If you are just running against the system version of python, just make sure nox is installed on the system or via the pipenv Pipfile. 
Any versions of python not found will just be skipped.
