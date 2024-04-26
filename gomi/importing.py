from __future__ import annotations


from typing import Optional
from types import ModuleType, FunctionType

__all__ = ["importMod", "importFunc"]


def importMod(module: str, package: Optional[str] = None) -> ModuleType:
    try:
        return __import__(module)
    except ImportError:
        input(f"Missing module `{module}`. " + (f"Try install `{package}`..." if package else ""))
        exit(1)


def importFunc(module: str, function: str, pkg_name: Optional[str] = None) -> FunctionType:
    try:
        return getattr(__import__(module), function)
    except ImportError:
        input(f"Missing module `{module}`. " + (f"Try install `{pkg_name}`..." if pkg_name else ""))
        exit(1)
    except AttributeError:
        input(f"Missing func `{function}` in module `{module}`" + (f" in package `{pkg_name}`" if pkg_name else "."))
        exit(1)
