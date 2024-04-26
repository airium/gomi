from __future__ import annotations

import sys  # fmt: skip
if sys.version_info < (3, 10):
    raise RuntimeError("This module requires Python 3.10.")

from types import ModuleType, FunctionType

__all__ = ["importMod", "importFunc"]


def importMod(module: str, package: str | None = None) -> ModuleType:
    try:
        return __import__(module)
    except ImportError:
        input(f"Missing module `{module}`. " + (f"Try install `{package}`..." if package else ""))
        exit(1)


def importFunc(module: str, function: str, pkg_name: str | None = None) -> FunctionType:
    try:
        return getattr(__import__(module), function)
    except ImportError:
        input(f"Missing module `{module}`. " + (f"Try install `{pkg_name}`..." if pkg_name else ""))
        exit(1)
    except AttributeError:
        input(f"Missing func `{function}` in module `{module}`" + (f" in package `{pkg_name}`" if pkg_name else "."))
        exit(1)
