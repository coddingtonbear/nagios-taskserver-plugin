import sys


def escape(value):
    return value.replace("|", "/").replace("\n", " ").strip()


def write_nagios_output(text, perfdata):
    if isinstance(text, basestring):
        text = text.split("\n")
    if isinstance(perfdata, basestring):
        perfdata = perfdata.split("\n")

    sys.stdout.write(escape(text[0]))
    if len(perfdata) > 0:
        sys.stdout.write("|")
        sys.stdout.write(escape(perfdata[0]))
    sys.stdout.write("\n")
    for idx, line in enumerate(text[1:]):
        sys.stdout.write(escape(line))
        if idx != len(text[1:]) - 1:
            sys.stdout.write("\n")
    if len(text[1:]) > 0:
        sys.stdout.write("|")
    for idx, line in enumerate(perfdata[1:]):
        sys.stdout.write(escape(line))
        sys.stdout.write("\n")
