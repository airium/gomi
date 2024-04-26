from __future__ import annotations

__all__ = ["MI", "MediaInfo", "parse", "getMediaInfo", "getMediaInfoList"]

from pathlib import Path
from multiprocessing import Pool

from pymediainfo import MediaInfo


def getMediaInfo(path: Path) -> MediaInfo:
    ret = MediaInfo.parse(path, output=None)
    if isinstance(ret, MediaInfo):
        return ret
    #! MI.parse() should only return `MediaInfo` if `output=None`, never str or something else.
    raise TypeError(f'MediaInfo.parse() returns unexpected "{type(ret)}" instead of "MediaInfo".')


def getMediaInfoList(paths: list[Path], mp: int = 1) -> list[MediaInfo]:
    mp = int(mp)
    if mp > 1:
        minfos = list(Pool().map(getMediaInfo, paths))
    else:
        minfos = list(map(getMediaInfo, paths))
    return minfos


parse = getMediaInfo
MI = MediaInfo
