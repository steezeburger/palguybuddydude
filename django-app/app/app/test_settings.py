from .settings import *

"""
Adds `common` app to installed apps so that test models are only created for tests.
"""
INSTALLED_APPS += ['common']
