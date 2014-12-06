import time

from taskw import TaskWarriorShellout


def main(*args):
    config_path = args[0]

    warrior = TaskWarriorShellout(
        config_filename=config_path
    )

    started = time.time()
    warrior.sync()
    finished = time.time()

    total_duration = finished - started

    return "Sync Successful", "%s" % total_duration
