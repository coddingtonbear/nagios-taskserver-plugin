import datetime
import json
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
    stdout, stderr = proc.communicate()
    with open('/tmp/taskcheck.out', 'w') as out:
        out.write(
            json.dumps(
                {
                    'stdout': stdout,
                    'stderr': stderr,
                    'retcode': proc.returncode,
                    'date': str(datetime.datetime.now())
                },
                indent=4
            )
        )
    if proc.returncode != 0:
        raise FailedToSynchronize(stderr)
    finished = time.time()

    total_duration = finished - started

    return "Sync Successful", "time=%ss;0.5;5.0;0;99" % total_duration
