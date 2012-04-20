#!/usr/bin/env python

import logging
import optparse
import sys

import analysis


if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option("-v", "--verbose", default=False, action="store_true")

    options, args = parser.parse_args()

    if options.verbose:
        logging.basicConfig(level=logging.DEBUG)

    if len(args) != 1:
        parser.print_usage()
        sys.exit(1)

    analysis.run.run_pipeline(args[0])
