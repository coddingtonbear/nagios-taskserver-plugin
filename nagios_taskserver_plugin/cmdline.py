from __future__ import print_function

import sys

from .main import main


EXIT_OK = 0
EXIT_WARNING = 1
EXIT_CRITICAL = 2
EXIT_UNKNOWN = 3


def cmdline():
    try:
        sys.stdout.write(main(sys.stdin.read()))
    except Exception as e:
        print(e)
        sys.exit(EXIT_UNKNOWN)
    sys.exit(EXIT_OK)
