import argparse
import logging
import subprocess
import time

from .exceptions import FailedToSynchronize
from .output import write_nagios_output


COMMANDS = {}


logger = logging.getLogger(__name__)


def command(fn):
    COMMANDS[fn.__name__] = fn


@command
def status(args):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'config_path',
        type=str
    )
    args = parser.parse_args(args)
    logger.info('Status check for taskrc at %s', args.config_path)

    started = time.time()
    cmd = [
        'task',
        'rc:%s' % args.config_path,
        'sync',
    ]
    logger.debug('Command: %s', cmd)
    proc = subprocess.Popen(
        cmd,
        shell=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    _, stderr = proc.communicate()
    logger.debug('Return Code: %s; Stderr: %s', proc.returncode, stderr)
    if proc.returncode != 0:
        raise FailedToSynchronize(
            " ".join(stderr.split('\n')[1:])
        )
    finished = time.time()

    total_duration = finished - started
    logger.debug('Finished in %s seconds', total_duration)

    write_nagios_output(
        "Sync Successful",
        "time=%ss;0.5;5.0;0;99" % total_duration
    )


@command
def restart(args):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'state',
        type=str
    )
    parser.add_argument(
        'state_type',
        type=str
    )
    parser.add_argument(
        'attempts',
        type=int
    )
    parser.add_argument(
        'restart_command',
        type=int
    )
    args = parser.parse_args(args)
    logger.info(
        'Conditional restart: %s;%s;%s "%s"',
        args.state,
        args.state_type,
        args.attempts,
        args.restart_command
    )

    is_soft_failure = (
        args.state == 'CRITICAL' and
        args.state_type == 'SOFT' and
        args.attempts >= 2
    )
    is_hard_failure = (
        args.state == 'CRITICAL' and
        args.state_type == 'HARD'
    )
    if is_soft_failure or is_hard_failure:
        logger.info(
            "Requesting restart; calling %s",
            args.restart_command,
        )
        try:
            subprocess.check_call(
                args.restart_command,
                shell=True,
            )
        except Exception as e:
            logger.exception(
                "Subprocess call failed!: %s", e
            )
