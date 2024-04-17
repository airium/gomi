import time
from typing import Optional


class TimeRecorder:
    def __init__(self, start=False):
        self._timings = []
        self._messages = []

        if start:
            self.mark("Immediately start at init")

    def mark(self, message: Optional[str] = None):
        self._timings.append(time.time())
        self._messages.append(message or "")

    def print(self, reset=False):
        if len(self._timings) < 2:
            print("No enough timings to print")
            return

        t_stt, t_end = self._timings[0], self._timings[-1]
        t_all = t_end - t_stt
        t_pre = self._timings[0]
        for i, (t_now, m) in enumerate(zip(self._timings, self._messages)):
            print(f"{i:>02d} @{t_now - t_stt:.3e} Δ{(dt := t_now - t_pre):.3e} ({dt/t_all:>5.1%}): {m}")
            t_pre = t_now

        if reset:
            self.reset()

    def reset(self):
        self._timings = []
        self._messages = []


TR = TimeRecorder
