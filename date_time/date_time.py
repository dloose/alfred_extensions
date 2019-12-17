#!/usr/bin/python

import sys
from subprocess import Popen, PIPE

import alfred


def get_time(title, format_string=None, tz=None):
    env = {}
    if tz:
        env["TZ"] = tz

    args = ["/bin/date"]
    if format_string and format_string[0] != "+":
        args.append("+" + format_string)

    try:
        p = Popen(args, env=env, stdout=PIPE)
        code = p.wait()
        if code != 0:
            result = "Invalid format"
        else:
            result = p.stdout.read().strip()
    except:
        result = "Error!"

    return dict(title=title, subtitle=result, arg=result)


if __name__ == "__main__":
    format_string = sys.argv[1] if len(sys.argv) > 1 else None

    feedback = alfred.Feedback()

    if not format_string:
        feedback.addItem(**get_time("Unix Timestamp", format_string="%s"))
        feedback.addItem(**get_time("Local ISO", format_string="%Y-%m-%dT%H:%M:%S%z"))
        feedback.addItem(**get_time("Local"))
        feedback.addItem(**get_time("GMT ISO", format_string="%Y-%m-%dT%H:%M:%S%z", tz="GMT"))
        feedback.addItem(**get_time("GMT", tz="GMT"))
    else:
        feedback.addItem(**get_time("Local", format_string=format_string))
        feedback.addItem(**get_time("GMT", format_string=format_string, tz="GMT"))

    feedback.output()

