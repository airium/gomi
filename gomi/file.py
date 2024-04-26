from __future__ import annotations

__all__ = ["getFileCRC32", "getFileSHA1", "File"]

import sys

if sys.version_info < (3, 9):
    raise RuntimeError("This module requires Python 3.9.")

import copy
import zlib
import hashlib
from os import PathLike
from pathlib import Path
from typing import Union

from .__utils import PathObj


_IO_SIZE = 16 * 2**20  # 16 MiB


def getFileCRC32(path: PathObj, prefix: str = "", read_size: int = _IO_SIZE, pass_error: bool = False) -> str:
    """
    path: PathObj: the Path to the file
    prefix: str: append to the front of the hash string

    readsize:int: the read size limit in bytes in each CRC32 update
    default is 16 MiB, using <=0 means full read without blocks
    a higher value may reduce the total time consumption as it reduces the IO times
    but when using a multi-processing reader, too large read size may cause OOM

    return:str: the hash string

    typical speed: 500-1500MB/s on NVMe SSD per thread
    """
    try:
        hash = 0
        with Path(path).open("rb") as fo:
            while b := fo.read(read_size):
                hash = zlib.crc32(b, hash)
        return f"{prefix}{hash:08x}"
    except Exception as e:
        if pass_error:
            return ""
        raise e


def getFileSHA1(path: PathObj, prefix: str = "", read_size: int = _IO_SIZE, pass_error: bool = False) -> str:
    """
    path: PathObj: the Path to the file
    prefix: str: append to the front of the hash string

    readsize:int: the read size limit in bytes in each SHA1 update
    default is 16 MiB, using <=0 means full read without blocks
    a higher value may reduce the total time consumption as it reduces the IO times
    but when using a multi-processing reader, too large read size may cause OOM

    return:str: the hash string

    typical speed: 500-2000MB/s on NVMe SSD per thread
    """
    try:
        hasher = hashlib.sha1()
        with Path(path).open("rb") as fo:
            while b := fo.read(read_size):
                hasher.update(b)
        return f"{prefix}{hasher.hexdigest()}"
    except Exception as e:
        if pass_error:
            return ""
        raise e


class File:

    "A read-only file object to access file information."

    def __init__(self, path: Union[str, PathLike], resolve: bool = True, caching: bool = True):

        path = Path(path).resolve() if resolve else Path(path)
        if not path.is_file():
            raise FileNotFoundError(f'File "{path}" not found')

        self.__path: Path = path
        self.__caching: bool = caching
        self.__cache: dict[str, str] = {}

    # * file system info -----------------------------------------------------------------------------------------------

    @property
    def path(self) -> Path:
        return copy.copy(self.__path)  #! disallow modification of any kind

    @property
    def posix(self) -> str:
        return self.__path.as_posix()

    @property
    def name(self) -> str:
        return self.__path.name

    @property
    def suffix(self) -> str:
        return self.__path.suffix

    @property
    def extension(self) -> str:
        return self.__path.suffix.lower().lstrip(".")

    @property
    def ext(self) -> str:
        return self.extension

    # * file information -----------------------------------------------------------------------------------------------

    @property
    def size(self) -> int:
        return self.__path.stat().st_size

    # * file hashing ---------------------------------------------------------------------------------------------------

    @property
    def crc32(self) -> str:
        if crc32 := self.__cache.get("crc32"):
            return crc32
        else:
            if crc32 := getFileCRC32(self.__path, pass_error=False):
                if self.__caching:
                    self.__cache["crc32"] = crc32
                return crc32
            raise RuntimeError(f'Unexpected failure on CRC32 calculation for file: "{self.__path}"')

    @property
    def sha1(self) -> str:
        if sha1 := self.__cache.get("sha1"):
            return sha1
        else:
            if sha1 := getFileSHA1(self.__path, pass_error=False):
                if self.__caching:
                    self.__cache["sha1"] = sha1
                return sha1
            raise RuntimeError(f'Unexpected failure on SHA1 calculation for file: "{self.__path}"')
