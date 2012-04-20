#!/usr/bin/env python

import logging

import analysis


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    analysis.run.run_pipeline('graph.ini')
