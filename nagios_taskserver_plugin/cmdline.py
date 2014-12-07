from __future__ import print_function

import sys

from .main import main, FailedToSynchronize


EXIT_OK = 0
EXIT_WARNING = 1
EXIT_CRITICAL = 2
EXIT_UNKNOWN = 3


def escape(value):
    return value.replace('|', '/').replace('\n', ' ').strip()


def write_nagios_output(text, perfdata):
    if isinstance(text, basestring):
        text = text.split('\n')
    if isinstance(perfdata, basestring):
        perfdata = perfdata.split('\n')

    sys.stdout.write(escape(text[0]))
    if len(perfdata) > 0:
        sys.stdout.write('|')
        sys.stdout.write(escape(perfdata[0]))
    sys.stdout.write('\n')
    for idx, line in enumerate(text[1:]):
        sys.stdout.write(escape(line))
        if idx != len(text[1:]) - 1:
            sys.stdout.write('\n')
    if len(text[1:]) > 0:
        sys.stdout.write('|')
    for idx, line in enumerate(perfdata[1:]):
        sys.stdout.write(escape(line))
        sys.stdout.write('\n')


def cmdline():
    try:
        text, perfdata = main(*sys.argv[1:])
        write_nagios_output(text, perfdata)
        sys.exit(EXIT_OK)
    except FailedToSynchronize as e:
        print(escape(str(e)))
        sys.exit(EXIT_CRITICAL)
    except Exception as e:
        print(escape(str(e)))
        sys.exit(EXIT_UNKNOWN)
