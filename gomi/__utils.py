from __future__ import annotations

__all__ = ["PathObj"]

from os import PathLike
from typing import Union
from pathlib import Path

PathObj = Union[str, PathLike, Path]
