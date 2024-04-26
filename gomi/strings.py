from __future__ import annotations

__all__ = ["YYMMDD", "HHMMSS", "YYMMDD_HHMMSS"]


import time


class _YYMMDD:

    def __str__(self) -> str:
        return time.strftime("%y%m%d", time.localtime())


class _HHMMSS:

    def __str__(self) -> str:
        return time.strftime("%H%M%S", time.localtime())


class _YYMMDD_HHMMSS:

    def __str__(self) -> str:
        return f"{YYMMDD}-{HHMMSS}"


YYMMDD = _YYMMDD()
HHMMSS = _HHMMSS()
YYMMDD_HHMMSS = _YYMMDD_HHMMSS()
