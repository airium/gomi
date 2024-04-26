from __future__ import annotations

__all__ = ["CustomHelpFormatter"]

import argparse


class CustomHelpFormatter(argparse.RawTextHelpFormatter):
    def __init__(self, prog, max_help_position: int = 50, width: int = 100):
        super().__init__(prog, max_help_position=max_help_position, width=width)

    def _format_action_invocation(self, action):
        if not action.option_strings or action.nargs == 0:
            return super()._format_action_invocation(action)
        default = self._get_default_metavar_for_optional(action)
        args_string = self._format_args(action, default)
        return ", ".join(action.option_strings) + " " + args_string
