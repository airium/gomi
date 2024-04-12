__all__ = ["hash"]

import hashlib

def hash(bchars: bytes, /) -> bytes:
    """Return the sha1 hash for the given bytes."""
    if isinstance(bchars, bytes):
        hasher = hashlib.sha1()
        hasher.update(bchars)
        return hasher.digest()
    else:
        raise TypeError(f"Expect bytes, not {type(bchars)}.")