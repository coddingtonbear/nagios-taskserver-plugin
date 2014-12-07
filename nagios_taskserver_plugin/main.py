import subprocess
import time


def main(*args):
    config_path = args[0]

    started = time.time()
    subprocess.call(
        'task',
        'rc:%s' % config_path,
        'sync',
        shell=True,
    )
    finished = time.time()

    total_duration = finished - started

    return "Sync Successful", "%s" % total_duration
