from __future__ import annotations

__all__ = ["rprint", "embolden", "pprint", "pdir"]

try:
    from pprint import pprint
except ImportError:
    print("pprint not found (pprint)")

try:
    import pdir
except ImportError:
    print("pdir not found (pdir2)")

from typing import Any
from os import linesep

INDENT_WIDTH = 4
MAX_DEPTH = 3


def embolden(text: Any) -> str:
    return f"\033[1m{text}\033[0m"


def _rprint(obj: Any, indent=0, newline=False):

    chars = ""

    if indent:
        chars += " " * indent

    otype = type(obj)
    if otype.__module__ == ("builtins"):
        chars += f"<{otype.__name__}>"
    else:
        chars += f"<{otype.__module__}.{otype.__qualname__}>"

    try:
        schars = f" | shape=[{'x'.join(map(str, obj.shape))}]"
    except Exception:
        pass
    else:
        chars += schars

    try:
        shape = obj.size()
    except Exception:
        pass
    else:
        chars += f" | size={shape}"
    try:
        shape = obj.size
    except Exception:
        pass
    else:
        chars += f" | size={shape}"
    try:
        chars += f" | len={len(obj)}"
    except Exception:
        pass

    try:
        dtype = obj.dtype
    except Exception:
        pass
    else:
        chars += f" | dtype={dtype}"

    try:
        device = obj.device
    except Exception:
        pass
    else:
        chars += f" | device=({device.type}:{device.index})"

    if isinstance(obj, int):
        chars += f" | {embolden(obj)}"
    elif isinstance(obj, float):
        chars += f" | {embolden(obj)}"
    elif isinstance(obj, str):
        chars += f' | "{embolden(obj)}"'

    print(chars, end=(linesep if newline else ""), flush=True)


def rprint(obj: Any, indent=0, self=True, depth=MAX_DEPTH):
    if self:
        _rprint(obj, indent=indent, newline=True)
    depth -= 1
    if depth < 0:
        print("Max depth reached. Stop.")
        return
    if isinstance(obj, list) or isinstance(obj, tuple):
        for i in obj:
            rprint(i, indent=indent + INDENT_WIDTH, depth=depth)
    elif isinstance(obj, dict):
        for k, v in obj.items():
            print(" " * (indent + INDENT_WIDTH) + embolden(k) + " : ", end="")
            _rprint(v, indent=0, newline=True)
            rprint(v, indent=indent + INDENT_WIDTH, self=False, depth=depth)
