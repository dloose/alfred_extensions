#!/usr/bin/python

import argparse
import base64
import sys
import urllib
import urlparse

import alfred


def wrap(entries):
    def wrapper(fn):
        def try_parse(s):
            try:
                return str(fn(s))
            except:
                return "Error!"
        return try_parse

    return [(key, wrapper(value)) for key, value in entries]


ENCODERS = wrap([
    ("Base64", base64.standard_b64encode),
    ("Base64 (URL safe)", base64.urlsafe_b64encode),
    ("URL", urllib.quote_plus),
])

DECODERS = wrap([
    ("Base64", base64.standard_b64decode),
    ("Base64 (URL safe)", base64.urlsafe_b64decode),
    ("URL", urlparse.parse_qs),
])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument(
        "--output-for-alfred", "-a",
        action  = "store_const",
        const   = True,
        default = False,
        help    = "Write the results as XML for Alfred. If this isn't present, the results are written 1 per line."
    )

    args, rest = parser.parse_known_args()

    if len(rest) != 2:
        sys.exit(1)

    cmd, data = rest

    if cmd not in ("encode", "decode"):
        sys.exit(1)

    fns = ENCODERS if cmd == "encode" else DECODERS

    result = [(key, fn(data)) for key, fn in fns]
    if args.output_for_alfred:
        feedback = alfred.Feedback()
        for key, value in result:
            feedback.addItem(title=key, subtitle=value, arg=value)
        feedback.output()
    else:
        for key, value in result:
            print "{}\t{}".format(key, value)
