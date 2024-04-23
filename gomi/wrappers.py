__all__ = ["tryCall", "tryMain", "tryTimedMain", "callTimed"]

import time
import traceback
from typing import Callable

from .strings import YYMMDD_HHMMSS
from .__i18n import *


__EXIT_WAIT = 5


def _exit_prompt(wait: int = 5):
    for i in range(max(wait, 1), 0, -1):
        print(EXITING_IN_1.format(time=i), end="\r")
        time.sleep(1)
    print(EXITING_0, end=" " * 10)


def tryCall(_callable: Callable, *args, **kwargs):
    try:
        return _callable(*args, **kwargs)
    except:
        traceback.print_exc()


def tryMain(_callable: Callable, *args, _exit_wait: int = __EXIT_WAIT, **kwargs):
    try:
        _callable(*args, **kwargs)
    except SystemExit as e:
        if e.code != 0:
            traceback.print_exc()
            input(HIT_EXCEP_0)
    except:
        traceback.print_exc()
        input(HIT_EXCEP_0)
    else:
        print(FINISHED_0)
        _exit_prompt(wait=_exit_wait)
        exit(0)
    finally:
        pass


def tryTimedMain(_callable: Callable, *args, _exit_wait: int = __EXIT_WAIT, **kwargs):
    try:
        print(STARTED_AT_1.format(time=YYMMDD_HHMMSS))
        _callable(*args, **kwargs)
    except SystemExit as e:
        if e.code != 0:
            traceback.print_exc()
            print(ERRORED_AT_1.format(time=YYMMDD_HHMMSS))
    except:
        traceback.print_exc()
        print(ERRORED_AT_1.format(time=YYMMDD_HHMMSS))
    else:
        print(FINISHED_AT_1.format(time=YYMMDD_HHMMSS))
        _exit_prompt(wait=_exit_wait)
        exit(0)
    finally:
        pass


def callTimed(_callable: Callable, *args, **kwargs):
    start = time.perf_counter()
    print(STARTED_AT_2.format(name=_callable.__name__, time=YYMMDD_HHMMSS))
    ret = _callable(*args, **kwargs)
    end = time.perf_counter()
    print(FINISHED_3.format(name=_callable.__name__, time=YYMMDD_HHMMSS, elapsed=end - start))
    return ret
