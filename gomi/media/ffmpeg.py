from __future__ import annotations


from typing import Union
from pathlib import Path


import shutil
from pathlib import Path

from .webp import _DEFAULT_WEBP_QUALITY
from .jpeg import _DEFAULT_JPEG_QUALITY
from ..fs import tryHardlink

import ffmpeg
import numpy as np


def tstFFmpegDecode(path: Path) -> bool:
    try:
        ffmpeg.input(path.resolve()).output("-", format="null").run(quiet=True)
    except ffmpeg._run.Error:
        return False
    return True


def tstFFmpegAudioDecode(path: Path, id: int = 0) -> bool:
    try:
        ffmpeg.input(path.resolve())[f"a:{id}"].output("-", format="null").run(quiet=True)
    except ffmpeg._run.Error:
        return False
    return True


def tstFFmpegVideoDecode(path: Path, id: int = 0) -> bool:
    try:
        ffmpeg.input(path.resolve())[f"v:{id}"].output("-", format="null").run(quiet=True)
    except ffmpeg._run.Error:
        return False
    return True


def ffprobe(path: Path) -> dict:
    try:
        return ffmpeg.probe(path.resolve())
    except ffmpeg._run.Error:
        return {}


def toWebp(
    src: Path,
    dst: Path,
    quality: int = _DEFAULT_WEBP_QUALITY,
    lossless: bool = False,
    resize: tuple[int, int] | None = None,
) -> bool:
    if not src.is_file():
        return False
    remove_dst = not dst.is_file()

    if resize:
        if resize[0] > 16383:
            resize = (16383, int(resize[1] * (16383 / resize[0])))
        if resize[1] > 16383:
            resize = (int(resize[0] * (16383 / resize[1])), 16383)
    if not (w_h := getDimension(src)):
        if remove_dst:
            dst.unlink(missing_ok=True)
        return False

    w, h = w_h
    if not resize and (w > 16383 or h > 16383):
        if w > 16383:
            w, h = 16383, (h * (16383 / w))
        if h > 16383:
            w, h = (w * (16383 / h)), 16383
        resize = (int(w), int(h))

    try:
        dst.parent.mkdir(parents=True, exist_ok=True)
        stream = ffmpeg.input(src.resolve().as_posix())
        if resize:
            stream = stream.filter("scale", *resize)
        stream = stream.output(
            dst.resolve().as_posix(),
            compression_level=12,
            quality=quality,
            lossless=int(lossless),
        )
        stream.run(quiet=True, overwrite_output=True)
    except ffmpeg._run.Error:
        if remove_dst:
            dst.unlink(missing_ok=True)
        return False
    return True


def toFLAC(src: Path, dst: Path) -> bool:
    if not src.is_file():
        return False
    remove_dst = not dst.is_file()
    try:
        stream = ffmpeg.input(src.resolve().as_posix())
        stream = stream.output(dst.resolve().as_posix(), compression_level=12)
        stream.run(quiet=True, overwrite_output=True)
    except ffmpeg._run.Error:
        if remove_dst:
            dst.unlink(missing_ok=True)
        return False
    return True


def toJPG(src: Path, dst: Path) -> bool:
    if not src.is_file():
        return False
    remove_dst = not dst.is_file()
    try:
        stream = ffmpeg.input(src.resolve().as_posix())
        stream = stream.output(dst.resolve().as_posix(), q=_DEFAULT_JPEG_QUALITY)
        stream.run(quiet=True, overwrite_output=True)
    except ffmpeg._run.Error:
        if remove_dst:
            dst.unlink(missing_ok=True)
        return False
    return True


def replaceIfSmaller(src: Path, dst: Path, bit: int, **kwds) -> bool:
    if not src.is_file():
        return False
    format = f"s{bit}le"
    acodec = f"pcm_s{bit}le"
    file_size = src.stat().st_size
    remove_dst = not dst.is_file()
    try:
        stream = ffmpeg.input(src.resolve().as_posix())
        stream = stream.output("pipe:", f="flac", compression_level=12, **kwds)
        output = stream.run(quiet=True, capture_stdout=True)[0]
    except ffmpeg._run.Error:
        if remove_dst:
            dst.unlink(missing_ok=True)
        return False
    try:
        dst.parent.mkdir(parents=True, exist_ok=True)
        if len(output) > file_size:
            if not tryHardlink(src, dst):
                shutil.copy2(src, dst)
        else:
            # TODO: high memory usage may occur when writing large files
            dst.write_bytes(output)
    except:
        if remove_dst:
            dst.unlink(missing_ok=True)
        return False
    return True


def getDimension(path: Path, idx: int = 0) -> tuple[int, int] | None:
    if not path.is_file():
        return None
    w, h = 0, 0
    try:
        if probe := ffprobe(path):
            if streams := probe.get("streams"):
                for stream in streams:
                    if stream.get("index") == idx:
                        w = stream.get("width", 0)
                        h = stream.get("height", 0)
    finally:
        return (w, h) if (w and h) else None


def readAudio(
    path: Path,
    id: Union[str, int] = 0,
    format: str = "s16le",
    start: int = 0,
    length: int = 0,
) -> np.ndarray:
    """
    Load the file from `path`
    Select audio track `id` and extract its first channel
    Read from `start` to `start+length` if `length`>0 else from `start` to the end
    Audio are always returned as PCM S16LE format to minimise memory cost
    """
    if length > 0:
        audio = np.frombuffer(
            ffmpeg.input(path.resolve())[f"a:{id}"]
            .filter("atrim", start_sample=start, end_sample=start + length)
            .output("-", ac=1, format=format, acodec="pcm_s16le")
            .run(capture_stdout=True, quiet=True)[0],
            np.int16,
        )
    else:
        audio = np.frombuffer(
            ffmpeg.input(path.resolve())[f"a:{id}"]
            .filter("atrim", start_sample=start)
            .output("-", ac=1, format=format, acodec="pcm_s16le")
            .run(capture_stdout=True, quiet=True)[0],
            np.int16,
        )
    return audio
