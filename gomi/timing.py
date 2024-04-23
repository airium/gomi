__all__ = ["TimeRecorder", "TR"]

import time
from typing import Optional
from .strings import YYMMDD_HHMMSS


class TimeRecorder:
    def __init__(self, start=False):
        self._timings = []
        self._messages = []

        if start:
            self.mark()

    def __len__(self):
        return len(self._messages)  #! dont change to len(self._timings)

    def mark(self, message: Optional[str] = None):
        self._timings.append(time.time())
        self._messages.append(message or (str(YYMMDD_HHMMSS) if (len(self) == 0) else "") or "")

    def print(self, reset=False):
        if len(self._timings) < 2:
            print("No enough timings to print")
            return

        t_stt = self._timings[0]
        t_all = self._timings[-1] - t_stt
        t_pre = self._timings[0]
        for i, (t_now, m) in enumerate(zip(self._timings[1:], self._messages[1:]), start=1):
            dt = t_now - t_pre
            print(f"{i:>02d} @{t_now - t_stt:.3e} Δ{dt:.3e} ({dt/t_all:>5.1%}): {m}")
            t_pre = t_now

        if reset:
            self.reset()

    def reset(self):
        self._timings = []
        self._messages = []


TR = TimeRecorder
