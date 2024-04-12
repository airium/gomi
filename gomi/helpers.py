import sys

import warnings
from typing import Sequence, Any

if sys.version_info >= (3, 10):
    # https://stackoverflow.com/a/3233356/14040883
    import collections.abc

    __all__ = ["updateMapping"]

    def updateMapping(d: dict, u: dict | collections.abc.Mapping):
        for k, v in u.items():
            if isinstance(v, collections.abc.Mapping):
                d[k] = updateMapping(d.get(k, {}), v)
            else:
                d[k] = v
                print(f"updated {k}={v}")
        return d

    def frange(start: int | float, stop: int | float | None = None, step: int | float = 1):
        start, stop = (0, start) if stop is None else (start, stop)
        if step <= 0:
            raise ValueError(f'step must be positive ,got "{step=}".')
        while start < stop:
            yield start
            start += step


def index(sequence: Sequence[Any], target: Any, case_sensitive: bool = False) -> int:
    if not case_sensitive:
        sequence = [(s.lower() if isinstance(s, str) else s) for s in sequence]
        target = target.lower() if isinstance(target, str) else target
    try:
        return sequence.index(target)
    except ValueError:
        return -1


def indexD(d: dict, key: Any, case_sensitive: bool = False) -> Any:
    keys = tuple(d.keys())
    i = index(keys, key, case_sensitive)
    if i > -1:
        return keys[i]
    elif key is None:
        return False  # avoid returning the same value
