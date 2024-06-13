from __future__ import annotations

__all__ = ["TimeRecorder", "TR"]

import time
from typing import Optional
from .strings import YYMMDD_HHMMSS


class TimeRecorder:
    def __init__(self, start: bool = False):
        self._timing_message_pairs: list[tuple[float, str]] = []

        if start:
            self.mark()

    def __len__(self):
        return len(self._timing_message_pairs)

    def mark(self, message: Optional[str] = None):
        _timing = time.time()
        _message = message or (str(YYMMDD_HHMMSS) if (len(self) == 0) else "")
        self._timing_message_pairs.append((_timing, _message))

    def print(self, reset: bool = False):
        if len(self._timing_message_pairs) < 2:
            print("No enough timings to print")
            return

        t_stt = self._timing_message_pairs[0][0]
        t_all = self._timing_message_pairs[-1][0] - t_stt
        t_pre = self._timing_message_pairs[0][0]
        for i, (t_now, msg) in enumerate(self._timing_message_pairs, start=0):
            dt = t_now - t_pre
            print(f"{i:>02d} @{t_now - t_stt:.3e} Δ{dt:.3e} ({dt/t_all:>5.1%}): {msg}")
            t_pre = t_now

        if reset:
            self.reset()

    def reset(self):
        self._timing_message_pairs.clear()


TR = TimeRecorder
