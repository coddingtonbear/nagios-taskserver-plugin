import argparse
import subprocess
import time

from .exceptions import FailedToSynchronize
from .output import write_nagios_output


COMMANDS = {}


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

    started = time.time()
    cmd = [
        'task',
        'rc:%s' % args.config_path,
        'sync',
    ]
    proc = subprocess.Popen(
        cmd,
        shell=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    _, stderr = proc.communicate()
    if proc.returncode != 0:
        raise FailedToSynchronize(
            " ".join(stderr.split('\n')[1:])
        )
    finished = time.time()

    total_duration = finished - started

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

    is_soft_failure = (
        args.state == 'CRITICAL' and
        args.state_type == 'SOFT' and
        args.attempts >= 3
    )
    is_hard_failure = (
        args.state == 'CRITICAL' and
        args.state_type == 'HARD'
    )
    if is_soft_failure or is_hard_failure:
        subprocess.check_call(
            args.restart_command,
            shell=True,
        )
