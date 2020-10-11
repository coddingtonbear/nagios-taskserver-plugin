import logging
import subprocess

from .exceptions import FailedToSynchronize, SynchronizationTimeout


logger = logging.getLogger(__name__)


def raise_synchronization_timeout(*args):
    raise SynchronizationTimeout()


def attempt_synchronization(config_path, task_binary="task"):
    cmd = [
        task_binary,
        "rc:%s" % config_path,
        "sync",
    ]
    logger.debug("Command: %s", cmd)
    proc = subprocess.Popen(
        cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    _, stderr = proc.communicate()
    logger.info("Return Code: %s; Stderr: %s", proc.returncode, stderr)
    if proc.returncode != 0:
        raise FailedToSynchronize(" ".join(stderr.split("\n")[1:]))
