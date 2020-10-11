from __future__ import print_function

import argparse
import logging
from pathlib import Path
import os
import sys
import tempfile

from .commands import COMMANDS
from .exceptions import FailedToSynchronize
from .output import escape


EXIT_OK = 0
EXIT_WARNING = 1
EXIT_CRITICAL = 2
EXIT_UNKNOWN = 3


logger = logging.getLogger(__name__)


def cmdline(sysargs=None):
    if not sysargs:
        sysargs = sys.argv[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument("command", type=str, choices=COMMANDS.keys())
    parser.add_argument("--log-level", type=logging.getLevelName, default="INFO")
    parser.add_argument(
        "--log-path",
        type=Path,
        default=os.path.join(tempfile.gettempdir(), "nagios-taskserver-plugin.log",),
    )
    args, extra = parser.parse_known_args(sysargs)

    logging.basicConfig(
        level=args.log_level, filename=args.log_path,
    )

    logger.info("Starting; incoming arguments: %s", sysargs)
    try:
        logger.debug(
            "Command: %s; Args: %s", args.command, extra,
        )
        COMMANDS[args.command](args=extra)
        sys.exit(EXIT_OK)
    except FailedToSynchronize as e:
        logger.error("Synchronization Failed.",)
        print(escape(str(e)))
        sys.exit(EXIT_CRITICAL)
    except Exception as e:
        logger.exception(
            "Exception encountered: %s", e,
        )
        print(escape(str(e)))
        sys.exit(EXIT_UNKNOWN)
