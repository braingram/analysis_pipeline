#!/usr/bin/env python
"""
Useful stuff for debugging graphs
"""

import logging


class DebugClass(object):
    """
    A simple debug class that spits out debugging messages
    using logging.debug when:
        created on __init__
        initialized on init
        run on __call__
    """
    def __init__(self, **kwargs):
        logging.debug("Debug(%s).__init__: %s" % (id(self), kwargs))

    def init(self, graph, **kwargs):
        logging.debug("Debug(%s).init: %s" % (id(self), graph))

    def __call__(self, *args, **kwargs):
        logging.debug("Debug(%s).run: %s" % (id(self), args))


def debug(*args, **kwargs):
    """
    A simple debug function that just prints out it's args and kwargs
    using logging.debug
    """
    logging.debug("debug: %s %s" % (args, kwargs))
