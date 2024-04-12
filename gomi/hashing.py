__all__ = ["toSHA1", "toCRC32"]

import sys

if sys.version_info < (3, 9):
    raise RuntimeError("This module requires Python 3.9.")

import hashlib
import zlib
from typing import Union


def toSHA1(bchars: Union[str, bytes], encoding: str = "utf-8") -> str:
    """Return the sha1 hash for the given bytes."""
    if isinstance(bchars, bytes):
        hasher = hashlib.sha1()
        hasher.update(bchars)
        return hasher.digest().hex()
    elif isinstance(bchars, str):
        return toSHA1(bchars.encode(encoding))
    else:
        raise TypeError(f'Unexpected type "{type(bchars)}".')


def toCRC32(bchars: Union[str, bytes], encoding: str = "utf-8") -> str:
    """Return the crc32 hash for the given bytes."""
    if isinstance(bchars, bytes):
        return zlib.crc32(bchars).to_bytes(4, "big").hex()
    elif isinstance(bchars, str):
        return toCRC32(bchars.encode(encoding))
    else:
        raise TypeError(f'Unexpected type "{type(bchars)}".')
