from __future__ import annotations

__all__ = ["DEBUG"]

import sys

DEBUG = hasattr(sys, "gettrace") and sys.gettrace() is not None
