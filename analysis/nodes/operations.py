#!/usr/bin/env python
"""
General pipeline operations
"""


def split(*args):
    """Split a list of arguments into seperate results"""
    return args


def merge(*args):
    """Merge a list of arguments into a single list"""
    return [args]


def iterate(*args):
    """Iterate over a list of arguments"""
    for arg in args:
        yield arg


def pprint(*args):
    for arg in args:
        print(arg)
