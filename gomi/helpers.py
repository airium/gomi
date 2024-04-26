from __future__ import annotations

__all__ = ["updateMapping", "frange", "index", "getkey"]


import sys  # fmt: skip
if sys.version_info < (3, 10):
    raise RuntimeError("This module requires Python 3.10.")


from typing import Sequence, Any
import collections.abc


def updateMapping(d: dict, u: dict | collections.abc.Mapping):
    """Recursively update a mapping with another mapping. See <https://stackoverflow.com/a/3233356/14040883>"""
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = updateMapping(d.get(k, {}), v)
        else:
            d[k] = v
    return d


def frange(start: int | float, stop: int | float | None = None, step: int | float = 1):
    """An alternative range function accepting float step."""
    start, stop = (0, start) if stop is None else (start, stop)
    if step <= 0:
        raise ValueError(f"step<0 is not allowed.")
    while start < stop:
        yield start
        start += step


def index(sequence: Sequence[Any], target: Any, case_sensitive: bool = False) -> int:
    """Find the index of the first occurrence of the target in sequence, else -1."""
    if not case_sensitive:
        sequence = [(s.lower() if isinstance(s, str) else s) for s in sequence]
        target = target.lower() if isinstance(target, str) else target
    try:
        return sequence.index(target)
    except ValueError:
        return -1


def getkey(d: dict[Any, Any], key: Any, case_sensitive: bool = False) -> Any:
    """Find if the key exists in the dict and return it, else return None.
    NOTE if key is None, return True/False denoting the existence of the key."""
    keys = tuple(d.keys())
    i = index(keys, key, case_sensitive=True)  #! respect the case first
    if i > -1:
        return keys[i] if (key is not None) else (keys[i] == key)
    if case_sensitive == False:
        i = index(keys, key, case_sensitive=False)
        if i > -1:
            return keys[i] if (key is not None) else (keys[i] == key)
