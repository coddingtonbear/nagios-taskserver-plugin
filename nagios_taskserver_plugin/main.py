import subprocess
import time


class FailedToSynchronize(Exception):
    pass


def main(*args):
    config_path = args[0]

    started = time.time()
    cmd = [
        'task',
        'rc:%s' % config_path,
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
        raise FailedToSynchronize(stderr)
    finished = time.time()

    total_duration = finished - started

    return "Sync Successful", "%s" % total_duration
