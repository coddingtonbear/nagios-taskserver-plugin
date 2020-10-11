import argparse
import logging
import signal
import subprocess
import time

from .exceptions import FailedToSynchronize
from .output import write_nagios_output
from .utils import attempt_synchronization, raise_synchronization_timeout


COMMANDS = {}


logger = logging.getLogger(__name__)


def command(fn):
    COMMANDS[fn.__name__] = fn


@command
def restart_if_failed(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("config_path", type=str)
    parser.add_argument("restart_command", type=str)
    parser.add_argument("--task-binary", type=str, default="task")
    parser.add_argument(
        "--timeout-seconds", type=int, default=30,
    )
    args = parser.parse_args(args)

    try:
        signal.signal(signal.SIGALRM, raise_synchronization_timeout)
        signal.alarm(args.timeout_seconds)

        attempt_synchronization(args.config_path, task_binary=args.task_binary)
        logger.info("Sync proceeded successfully.")

        # Reset the alarm
        signal.alarm(0)
    except FailedToSynchronize:
        logger.info("Sync failed; issuing restart.")
        try:
            subprocess.check_call(
                args.restart_command, shell=True,
            )
        except Exception as e:
            logger.exception("Subprocess call failed!: %s", e)


@command
def status(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("config_path", type=str)
    args = parser.parse_args(args)
    logger.info("Status check for taskrc at %s", args.config_path)

    started = time.time()
    attempt_synchronization(args.config_path)
    finished = time.time()

    total_duration = finished - started
    logger.debug("Finished in %s seconds", total_duration)

    write_nagios_output("Sync Successful", "time=%ss;0.5;5.0;0;99" % total_duration)


@command
def restart(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("state", type=str)
    parser.add_argument("state_type", type=str)
    parser.add_argument("attempts", type=int)
    parser.add_argument("restart_command", type=str)
    args = parser.parse_args(args)
    logger.info(
        'Conditional restart: %s;%s;%s "%s"',
        args.state,
        args.state_type,
        args.attempts,
        args.restart_command,
    )

    is_soft_failure = (
        args.state == "CRITICAL" and args.state_type == "SOFT" and args.attempts >= 2
    )
    is_hard_failure = args.state == "CRITICAL" and args.state_type == "HARD"
    logger.debug(
        "Hard failure? %s; Soft failure? %s", is_hard_failure, is_soft_failure,
    )
    if is_soft_failure or is_hard_failure:
        logger.info(
            "Requesting restart; calling %s", args.restart_command,
        )
        try:
            subprocess.check_call(
                args.restart_command, shell=True,
            )
        except Exception as e:
            logger.exception("Subprocess call failed!: %s", e)
