class FailedToSynchronize(Exception):
    pass


class SynchronizationTimeout(FailedToSynchronize):
    pass
