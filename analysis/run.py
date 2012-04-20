#!/usr/bin/env python

import logging

import cconfig

import graph


def run_pipeline(cfgfile, options=[]):
    cfg = cconfig.TypedConfig(local=cfgfile, options=options)
    g = graph.load.load(cfg.get('pipeline', 'graph'))

    logging.debug("Start node: %s" % graph.movement.find_start(g))

    logging.debug("====== PARSE =======")
    graph.load.parse_nodes(g, cfg)

    logging.debug("====== INIT =======")
    graph.movement.call_graph(g, 'init')

    logging.debug("====== RUN =======")
    graph.movement.call_graph(g, '__call__')

    return g
