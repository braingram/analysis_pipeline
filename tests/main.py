#!/usr/bin/env python

# pre-hook
# check/analyze
#   for file in raw/:
#       is result valid?
#           NO  -> run analysis
#           YES -> skip
# post-hook

# plugins might have
# pre-hook (optional)
# check_result
# analyze
# post-hook (optional)

# main program:
# load plugins
# run plugins

import logging
import os

# load plugins
import plugins

logging.basicConfig(level=logging.DEBUG)

OUTPUT_DIR = "./output"
INPUT_DIR = "./input"
LOG_FILE = "./log"

logging.basicConfig(level = logging.DEBUG,
        filename = LOG_FILE, filemode = 'a')

# default plugin options
DEFAULT_OPTIONS = {}

# make these real paths
OUTPUT_DIR = os.path.realpath(OUTPUT_DIR)
INPUT_DIR = os.path.realpath(INPUT_DIR)

plugin_names = plugins.__all__

for plugin_name in plugin_names:
    plugin = plugins.__dict__[plugin_name]
    if not ('options' in plugin.__dict__.keys()):
        plugin.options = DEFAULT_OPTIONS
    
    if plugin.options.get('private_directory', False):
        plugin_input_directory = '/'.join((INPUT_DIR, plugin_name))
        plugin_output_directory = '/'.join((OUTPUT_DIR, plugin_name))
    else:
        plugin_input_directory = INPUT_DIR
        plugin_output_directory = OUTPUT_DIR

    # make i/o directories
    if not(os.path.exists(plugin_input_directory)):
        os.makedirs(plugin_input_directory)
    if not(os.path.exists(plugin_output_directory)):
        os.makedirs(plugin_output_directory)

    # run the pre_hook function if it exists
    if 'pre_hook' in plugin.__dict__.keys():
        # TODO check return value
        plugin.pre_hook(plugin_input_directory,\
                plugin_output_directory)
    else:
        logging.debug("Plugin %s does not contain pre_hook" % plugin_name)

    # check the validity of the plugin
    if not ('check_result' in plugin.__dict__.keys()):
        raise IOError(\
                'Plugin %s does not contain the required check_result function'\
                % plugin_name)
    if not ('analyze' in plugin.__dict__.keys()):
        raise IOError(\
                'Plugin %s does not contain the required analyze function'\
                % plugin_name)

    # filter input files by filename
    input_filename_filter = plugin.__dict__.get(\
            'input_filename_filter', lambda x: True)
    
    # check the result of each input file
    for input_filename in os.listdir(plugin_input_directory):
        if not (input_filename_filter(input_filename)):
            # skip files that don't pass the filter
            continue

        real_input_filename = '/'.join((plugin_input_directory,input_filename))
        if plugin.check_result(real_input_filename, plugin_output_directory):
            # TODO check return value
            plugin.analyze(real_input_filename, plugin_output_directory)

    # run the post_hook function if it exists
    if 'post_hook' in plugin.__dict__.keys():
        # TODO check return value
        plugin.post_hook(plugin_input_directory,\
                plugin_output_directory)
    else:
        logging.debug("Plugin %s does not contain post_hook" % plugin_name)

