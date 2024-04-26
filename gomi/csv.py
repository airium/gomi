from __future__ import annotations

__all__ = ["writeCSV", "readCSV"]

import os
import csv
import string
from pathlib import Path
from typing import Optional

from .chars import quote, unquote


_CSV_QUOT_CHAR = '"'


def writeCSV(csv_path: Path, data: list[dict], encoding: str = "utf-8-sig", newline: str = os.linesep) -> bool:

    try:
        csv_path = Path(csv_path)
        assert csv_path.suffix.lower() == ".csv"
        assert len(data) > 0 and all(isinstance(d, dict) for d in data)
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        csv_head = data[0].keys()
        with csv_path.open("w", encoding=encoding, newline="") as fo:
            w = csv.DictWriter(fo, csv_head, lineterminator=newline, delimiter=",")
            w.writeheader()
            w.writerows(data)
    except:
        return False
    return True


def readCSV(csv_path: Path, encoding: str = "utf-8-sig", newline: str = os.linesep) -> tuple[bool, list[dict]]:

    if not (csv_path := Path(csv_path)).is_file():
        return False, []

    try:
        with csv_path.open("r", encoding=encoding, newline=newline) as fo:
            reader = csv.DictReader(fo)
            data = [info for info in reader]
    except:
        return False, []
    return True, data


def quoteCSVFields(entries: list[dict], quot_mark: Optional[str] = None, sep: Optional[str] = None) -> list[dict]:
    """Return a copy of the input list of dict, with all chars quoted."""

    if not entries:
        return []
    quot_mark = _CSV_QUOT_CHAR if quot_mark is None else quot_mark
    sep = "," if sep == None else sep

    ret: list[dict] = []
    for entry in entries:
        d = {}
        for k, v in entry.items():
            if isinstance(v, str) and v and all(c in string.hexdigits for c in v):
                v = quote(v, quot_mark)
            elif isinstance(v, str) and v and (sep in v):
                v = quote(v, quot_mark)
            elif not isinstance(v, str):
                v = quote(v, quot_mark)
            d[k] = v
        ret.append(d)

    return ret


def unquoteCSVFields(entries: list[dict[str, str]], quot_mark: Optional[str] = None) -> list[dict[str, str]]:
    quot_mark = _CSV_QUOT_CHAR if quot_mark is None else quot_mark
    ret = []
    for entry in entries:
        d = {}
        for k, v in entry.items():
            d[k] = unquote(v, quot_mark)
        ret.append(d)
    return ret
