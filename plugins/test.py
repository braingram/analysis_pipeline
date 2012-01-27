#!/usr/bin/env python

import logging

options = {} # plugin options

def pre_hook(input_directory, output_directory):
    logging.debug("pre_hook called in test plugin: %s %s" %\
            (input_directory, output_directory))

def input_filename_filter(input_filename):
    """ True: process file, False: skip file """
    logging.debug("input_filename_filter called in test plugin: %s" % \
            input_filename)
    return True

def check_result(input_filename, output_directory):
    """ True: process file, False: skip file """
    logging.debug("check_result called in test plugin: %s %s" % \
            (input_filename, output_directory))
    return True

def analyze(input_filename, output_directory):
    logging.debug("analyze called in test plugin: %s %s" % \
            (input_filename, output_directory))

def post_hook(input_directory, output_directory):
    logging.debug("post_hook called in test plugin: %s %s" %\
            (input_directory, output_directory))
