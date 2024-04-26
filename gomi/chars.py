from __future__ import annotations

__all__ = ["unquote", "quote", "isDecimal"]

from typing import Optional


_QUOT_MARK = '"'


def unquote(chars: str, quot_mark: Optional[str] = None) -> str:
    if not chars:
        return ""
    quot_mark = _QUOT_MARK if quot_mark is None else quot_mark
    if not quot_mark:
        return chars
    while chars.startswith(quot_mark) and chars.endswith(quot_mark):
        chars = chars[len(quot_mark) : -len(quot_mark)]
    return chars


def quote(chars: str, quot_mark: Optional[str] = None) -> str:
    if not chars:
        return ""
    quot_mark = _QUOT_MARK if quot_mark is None else quot_mark
    return f"{quot_mark}{unquote(chars, quot_mark)}{quot_mark}"


def isDecimal(chars: str) -> bool:
    return chars.replace(".", "", 1).isdigit()
