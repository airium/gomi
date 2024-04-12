__all__ = ["tryCall", "tryMain", "tryTimedMain", "callTimed"]

import time
import traceback
from typing import Callable
from .strings import YYMMDD_HHMMSS

_START_1 = "Started at {time}"
_START_2 = "{name} started at {time}"
_FINISH_0 = "Finished."
_FINISH_3 = "{name} finished at {time}, elapsed {elapsed:.3f}s"
_FINISH_WE_1 = "Interrupted at {time} WITH EXCEPTION."
_FINISH_WO_1 = "Finished at {time} without uncaught exception."
_HIT_EXP_0 = "↑↑↑ Hit uncaught exception! Please check/report ↑↑↑"
_EXITING_0 = "Exiting ...          "
_EXITING_1 = "Exiting in {time}s..."

__EXIT_WAIT = 5


def _exit_prompt(wait: int = 5):
    for i in range(max(wait, 1), 0, -1):
        print(_EXITING_1.format(time=i), end="\r")
        time.sleep(1)
    print(_EXITING_0)


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
            input(_HIT_EXP_0)
    except:
        traceback.print_exc()
        input(_HIT_EXP_0)
    else:
        print(_FINISH_0)
        _exit_prompt(wait=_exit_wait)
        exit(0)
    finally:
        pass


def tryTimedMain(_callable: Callable, *args, _exit_wait: int = __EXIT_WAIT, **kwargs):
    try:
        print(_START_1.format(time=YYMMDD_HHMMSS))
        _callable(*args, **kwargs)
    except SystemExit as e:
        if e.code != 0:
            traceback.print_exc()
            print(_FINISH_WE_1.format(time=YYMMDD_HHMMSS))
    except:
        traceback.print_exc()
        print(_FINISH_WE_1.format(time=YYMMDD_HHMMSS))
    else:
        print(_FINISH_WO_1.format(time=YYMMDD_HHMMSS))
        _exit_prompt(wait=_exit_wait)
        exit(0)
    finally:
        pass


def callTimed(_callable: Callable, *args, **kwargs):
    start = time.perf_counter()
    print(_START_2.format(name=_callable.__name__, time=YYMMDD_HHMMSS))
    ret = _callable(*args, **kwargs)
    end = time.perf_counter()
    print(_FINISH_3.format(name=_callable.__name__, time=YYMMDD_HHMMSS, elapsed=end - start))
    return ret
