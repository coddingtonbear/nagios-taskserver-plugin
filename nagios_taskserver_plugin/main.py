import subprocess
import time


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
    _, _ = proc.communicate()
    finished = time.time()

    total_duration = finished - started

    return "Sync Successful", "%s" % total_duration
