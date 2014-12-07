import subprocess


class FailedToSynchronize(Exception):
    pass


def main(*args):
    config_path = args[0]

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

    return "Sync Successful"
