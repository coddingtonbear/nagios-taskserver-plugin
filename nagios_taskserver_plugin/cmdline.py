from __future__ import print_function

import argparse
import sys

from .commands import COMMANDS
from .exceptions import FailedToSynchronize
from .output import escape


EXIT_OK = 0
EXIT_WARNING = 1
EXIT_CRITICAL = 2
EXIT_UNKNOWN = 3


def cmdline(sysargs=None):
    if not sysargs:
        sysargs = sys.argv[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'command',
        type=str,
        choices=COMMANDS.keys()
    )
    args, extra = parser.parse_known_args(sysargs)
    try:
        COMMANDS[args.command](args=extra)
        sys.exit(EXIT_OK)
    except FailedToSynchronize as e:
        print(escape(str(e)))
        sys.exit(EXIT_CRITICAL)
    except Exception as e:
        print(escape(str(e)))
        sys.exit(EXIT_UNKNOWN)
