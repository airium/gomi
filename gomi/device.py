from __future__ import annotations

from pathlib import Path
from logging import Logger
from typing import Optional

import ssd_checker

from .__i18n import FOUND_SSD_1, FOUND_HDD_1, SSD_CHECKER_KEY_ERROR_1, SSD_CHECKER_UNK_ERROR_2


def isSSD(path: Path, fallback: bool = False, logger: Optional[Logger] = None) -> bool:
    try:
        ret = ssd_checker.is_ssd(path.resolve().as_posix())
        if logger:
            logger.debug(FOUND_SSD_1.format(path) if ret else FOUND_HDD_1.format(path))
        return ret
    except KeyError:
        if logger:
            logger.debug(SSD_CHECKER_KEY_ERROR_1.format(path))
        # this happens when the input path is an SCSI device which is not listed as system physical drives
        return fallback
    except Exception as e:
        if logger:
            logger.debug(SSD_CHECKER_UNK_ERROR_2.format(e, path))
        return fallback
