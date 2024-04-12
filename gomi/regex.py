__all__ = ["extract1", "extractN"]

import re
from typing import Optional


def extract1(pattern: re.Pattern | str, text: str, group: Optional[str | int] = None) -> str | None:
    if match := re.search(pattern, text):
        if group:
            return match.group(group)
        return match.group(0)
    return None


def extractN(pattern, text, group, idx) -> list[str] | None:
    raise NotImplementedError
