from __future__ import annotations

__all__ = ["readPickle", "writePickle", "readPKL", "writePKL", "getSize"]

import pickle
from pathlib import Path

_ENCODINGS = ("ASCII", "UTF-8", "Latin1")


def readPickle(path, encoding=None):
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f'File "{path}" not found')
    if isinstance(encoding, str) and encoding:
        return pickle.loads(Path(path).read_bytes(), encoding=encoding)
    elif encoding is None:
        for encoding in _ENCODINGS:
            try:
                return pickle.loads(Path(path).read_bytes(), encoding=encoding)
            except UnicodeDecodeError:
                pass
        raise UnicodeError(f'Failed to decode pickle file "{path}"')
    else:
        raise ValueError(f'Invalid "{path}"')


readPKL = readPickle


def writePickle(obj, path, overwrite=False):
    path = Path(path)
    if not overwrite and path.is_file():
        raise FileExistsError(f'File "{path}" already exists')
    path.parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_bytes(pickle.dumps(obj))


writePKL = writePickle


def getSize(obj) -> int:
    size = len(pobj := pickle.dumps(obj))
    del pobj
    return size
