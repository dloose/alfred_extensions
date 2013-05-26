#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import fnmatch
import os
from subprocess import Popen, PIPE

import alfred

from pprint import pprint

__version__ = (1, 0, 1)

class ScreenSharing(object):
    def __init__(self):
        self.cache = alfred.Cache()

    def run(self):
        machine = alfred.argv(1)

        if machine is None:
            machine = ""

        machine = machine.strip()

        dir = os.path.expanduser( "~/Library/Application Support/Screen Sharing/" )
        pattern = "%s*.vncloc" % (machine)
        matches = [ f for f in os.listdir( dir ) if fnmatch.fnmatch( f, pattern ) ]

        feedback = alfred.Feedback()
        if len( matches ) > 0:
            for file in matches:
                feedback.addItem(
                    title = "Start Screen Sharing with %s" % (os.path.splitext( file )[0]),
                    arg   = os.path.join( dir, file )
                    )
        elif machine != "":
            feedback.addItem(
                title = "Start Screen Sharing with %s" % (machine),
                arg   = "vnc://%s" % (machine)
                )

        feedback.output()

if __name__ == '__main__':
    ScreenSharing().run()
