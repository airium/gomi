"""
This module is modified from `scionoftech/webptools` <https://github.com/scionoftech/webptools> (MIT License).
This version includes improvement and additional functions.
"""

from __future__ import annotations

import platform
import subprocess
from os import PathLike
from typing import Optional, Union
from pathlib import Path

from ..chars import quote

import webptools

PathObj = Union[str, PathLike]
WEBTOOLS_MOD_LIB = Path(webptools.__file__).absolute().parent.parent / "lib"

_DEFAULT_WEBP_QUALITY = 90


__all__ = ["get_cwebp_bin", "get_dwebp_bin", "get_webpquality_bin", "cwebp", "dwebp", "test_dwebp", "webpquality"]


def get_cwebp_bin(bin_path: Optional[PathObj] = None) -> str:
    if bin_path is None:
        match platform.system():
            case "Linux":
                return (WEBTOOLS_MOD_LIB / "libwebp_linux/bin/cwebp").as_posix()
            case "Windows":
                match platform.architecture()[0]:
                    case "64bit":
                        return (WEBTOOLS_MOD_LIB / "libwebp_win64/bin/cwebp.exe").as_posix()
                    case "32bit" | "86bit":
                        raise NotImplementedError("Unsupported platform:", platform.system(), platform.architecture())
                    case _:
                        raise NotImplementedError("Unsupported platform:", platform.system(), platform.architecture())
            case "Darwin":
                return (WEBTOOLS_MOD_LIB / "libwebp_osx/bin/cwebp").as_posix()
            case _:
                raise OSError("Unsupported platform:", platform.system(), platform.architecture())
    elif isinstance(bin_path, Path):
        return f"{Path(WEBTOOLS_MOD_LIB).as_posix()}"
    elif isinstance(bin_path, str):
        return bin_path
    else:
        raise TypeError(f"Unsupported input type {type(bin_path)}")


def get_dwebp_bin(bin_path: Optional[Union[str, Path]] = None) -> str:
    if bin_path is None:
        match platform.system():
            case "Linux":
                return (WEBTOOLS_MOD_LIB / "libwebp_linux/bin/dwebp").as_posix()
            case "Windows":
                match platform.architecture()[0]:
                    case "64bit":
                        return (WEBTOOLS_MOD_LIB / "libwebp_win64/bin/dwebp.exe").as_posix()
                    case "32bit" | "86bit":
                        raise NotImplementedError("Unsupported platform:", platform.system(), platform.architecture())
                    case _:
                        raise NotImplementedError("Unsupported platform:", platform.system(), platform.architecture())
            case "Darwin":
                return (WEBTOOLS_MOD_LIB / "libwebp_osx/bin/dwebp").as_posix()
            case _:
                raise OSError("Unsupported platform:", platform.system(), platform.architecture())
    elif isinstance(bin_path, Path):
        return f"{Path(WEBTOOLS_MOD_LIB).as_posix()}"
    elif isinstance(bin_path, str):
        return bin_path
    else:
        raise TypeError(f"Unsupported input type {type(bin_path)}")


def get_webpquality_bin(bin_path: Optional[PathObj] = None) -> str:
    if bin_path is None:
        match platform.system():
            case "Linux":
                return (WEBTOOLS_MOD_LIB / "libwebp_linux/bin/webp_quality").as_posix()
            case "Windows":
                match platform.architecture()[0]:
                    case "64bit":
                        return (WEBTOOLS_MOD_LIB / "libwebp_win64/bin/webp_quality.exe").as_posix()
                    case "32bit" | "86bit":
                        raise NotImplementedError("Unsupported platform:", platform.system(), platform.architecture())
                    case _:
                        raise NotImplementedError("Unsupported platform:", platform.system(), platform.architecture())
            case "Darwin":
                return (WEBTOOLS_MOD_LIB / "libwebp_osx/bin/webp_quality").as_posix()
            case _:
                raise OSError("Unsupported platform:", platform.system(), platform.architecture())
    elif isinstance(bin_path, Path):
        return f"{Path(WEBTOOLS_MOD_LIB).as_posix()}"
    elif isinstance(bin_path, str):
        return bin_path
    else:
        raise TypeError(f"Unsupported input type {type(bin_path)}")


def cwebp(input_path: str, output_path: str, option: str, logging: str = "-v", bin_path: str | None = None) -> dict:
    """Modified from webptools.cwebp"""

    bin_path = quote(bin_path if bin_path else get_cwebp_bin(bin_path=bin_path))
    input_path = quote(input_path)
    cmd = f"{bin_path} {option} {logging} {input_path} -o {output_path}"
    p = subprocess.Popen(cmd, shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (stdout, stderr) = p.communicate()
    result = {"exit_code": p.returncode, "stdout": stdout, "stderr": stderr, "command": cmd}
    return result


def dwebp(input_path: str, output_path: str, option: str, logging: str = "-v", bin_path: str | None = None) -> dict:
    """Modified from webptools.dwebp"""

    bin_path = quote(bin_path if bin_path else get_dwebp_bin(bin_path=bin_path))
    input_path = quote(input_path)
    cmd = f"{bin_path} {option} {logging} {input_path} -o {output_path}"
    p = subprocess.Popen(cmd, shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (stdout, stderr) = p.communicate()
    # result = {'exit_code': p.returncode, 'stdout': stdout, 'stderr': stderr, 'command': cmd}
    result = {"exit_code": p.returncode, "stdout": "", "stderr": stderr, "command": cmd}  # we don't need the output
    return result


def test_dwebp(input_path: str, bin_path: str | None = None) -> dict:
    """Modified from webptools.dwebp"""

    bin_path = quote(bin_path if bin_path else get_dwebp_bin(bin_path=bin_path))
    input_path = quote(input_path)
    cmd = f"{bin_path} {input_path}"
    p = subprocess.Popen(cmd, shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (stdout, stderr) = p.communicate()
    result = {"exit_code": p.returncode, "stdout": stdout, "stderr": stderr, "command": cmd}
    return result


def webpquality(webp_path: str, bin: Optional[str] = None) -> int:
    """
    Estimate the quality of a WebP image with `webp_quality`.
    Return the estimated `q` value, or 0 if failed.
    """

    bin = quote(bin if bin else get_webpquality_bin(bin_path=bin))
    webp_path = quote(webp_path)
    cmd = f"{bin} -quiet {webp_path}"
    p = subprocess.Popen(cmd, shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (stdout, stderr) = p.communicate()
    result = {"exit_code": p.returncode, "stdout": stdout, "stderr": stderr, "command": cmd}

    try:
        return int(result["stdout"])
    except ValueError:
        return 0
