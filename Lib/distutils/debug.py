import os

# This module should be kept compatible with Python 1.5.2.

__revision__ = "$Id$"

# If DISTUTILS_DEBUG is anything other than the empty string, we run in
# debug mode.
DEBUG = os.environ.get('DISTUTILS_DEBUG')

