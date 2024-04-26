from __future__ import annotations

__all__ = ["preparePath", "readFile", "writeFile", "read", "write"]

from pathlib import Path
from typing import Optional, Union

from .__utils import PathObj


def preparePath(path: PathObj, filename: str, overwrite: bool = False) -> Path:
    path = Path(path)
    if path.is_file():
        if not overwrite:
            raise FileExistsError(f"File already exists: {path}")
    elif path.is_dir():
        path = path / filename
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
    return path


def readFile(path: PathObj, encoding: Optional[str] = None) -> str | bytes:
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"File not found: {path}")
    if encoding:
        return path.read_text(encoding=encoding)
    else:
        return path.read_bytes()


read = readFile


def writeFile(path: PathObj, data: Union[str, bytes], encoding: Optional[str] = None):
    path = Path(path)
    if encoding and isinstance(data, str):
        path.write_text(data, encoding=encoding)
    elif isinstance(data, str):
        raise ValueError("Encoding must be provided for data of type 'str'")
    elif isinstance(data, bytes):
        path.write_bytes(data)
    else:
        raise ValueError(f"Invalid type of data: {type(data)}")


write = writeFile
