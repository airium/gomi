from __future__ import annotations

__all__ = ["extract1", "extractN"]

import re
from typing import Optional, Union


def extract1(pattern: Union[re.Pattern, str], text: str, group: Optional[Union[str, int]] = None) -> Optional[str]:
    if match := re.search(pattern, text):
        if group:
            return match.group(group)
        return match.group(0)
    return None


reget_1 = extract1


def extractN(pattern, text, group, idx) -> Optional[list[str]]:
    raise NotImplementedError


reget_n = extractN
