from __future__ import print_function

import sys

from .main import main, FailedToSynchronize


EXIT_OK = 0
EXIT_WARNING = 1
EXIT_CRITICAL = 2
EXIT_UNKNOWN = 3


def escape(value):
    return value.replace('|', '/').replace('\n', ' ').strip()


def cmdline():
    try:
        print(escape(main(*sys.argv[1:])))
        sys.exit(EXIT_OK)
    except FailedToSynchronize as e:
        print(escape(str(e)))
        sys.exit(EXIT_CRITICAL)
    except Exception as e:
        print(escape(str(e)))
        sys.exit(EXIT_UNKNOWN)
