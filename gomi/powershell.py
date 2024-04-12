__all__ = ["powershell"]

import sys  # fmt: skip
if sys.version_info < (3, 6):
    raise RuntimeError("This module requires Python 3.6.")

from subprocess import call


def powershell(cmd: str, asAdmin: bool = False):
    if asAdmin:
        call(f"PowerShell -Command \"Start-Process -Verb RunAs PowerShell -Arg '{cmd}'\"", shell=True)
    else:
        call(f'PowerShell -Command "{cmd}"', shell=True)
