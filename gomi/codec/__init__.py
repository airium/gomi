import sys
import warnings

if sys.version_info < (3, 10):
    warning.warn('gomi.codec requires Python 3.10 or higher')
else:
    from .bencoder import *
