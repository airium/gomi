from __future__ import annotations

__all__ = ["findProcess"]


def findProcess(name: str, exact: bool = True) -> bool:
    import psutil

    if exact:
        for process in psutil.process_iter():
            if process.name().lower() == name.lower():
                return True
    else:
        for process in psutil.process_iter():
            if process.name().lower().startswith(name.lower()):
                return True
    return False
