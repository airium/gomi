from __future__ import annotations

__all__ = ["toNamedTuple"]

from collections import namedtuple
from typing import Optional


def toNamedTuple(d: dict, name: Optional[str] = None):
    assert isinstance(d, dict)
    return namedtuple(name or "AnonymousNamedTuple", d.keys())(**d)
