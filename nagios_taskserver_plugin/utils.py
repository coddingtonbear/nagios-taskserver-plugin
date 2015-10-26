import logging
import subprocess

from .exceptions import FailedToSynchronize


logger = logging.getLogger(__name__)


def attempt_synchronization(config_path):
    cmd = [
        'task',
        'rc:%s' % config_path,
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
