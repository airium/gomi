__all__ = ["relative2gomi"]

import importlib.util
import importlib.machinery
from pathlib import Path

_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0"


def relative2gomi(path: Path) -> str:
    return Path(path).relative_to(importlib.util.find_spec("gomi").origin).with_suffix("").as_posix()
