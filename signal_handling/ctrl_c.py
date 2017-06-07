#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# this module showns how to define a new signal handler
# our example handles CTRL-C signal redirecting it to signal_handler()
#
#
import signal
import sys

def signal_handler(signum, frame):
    """
    :param signum is the signal number
    :param frame is current stack frame
    """
    print 'You pressed Ctrl+C! Generating a signal with number #', signum
    sys.exit(0)

"""
   register the function that will handle the signal
   ref. https://docs.python.org/2/library/signal.html
"""
signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C')

"""Cause the process to sleep until a signal is received
"""
#signal.pause()

while True:
    pass