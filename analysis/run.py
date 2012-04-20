#!/usr/bin/env python

import logging

import cconfig

import graph


def run_pipeline(cfgfile):
    cfg = cconfig.TypedConfig(local=cfgfile)
    g = graph.io.load(cfg.get('pipeline', 'graph'))

    logging.debug("Start node: %s" % graph.movement.find_start(g))

    logging.debug("====== PARSE =======")
    graph.io.parse_nodes(g, cfg)

    logging.debug("====== INIT =======")
    graph.movement.walk_graph(g, 'init', args=[g, ])

    logging.debug("====== RUN =======")
    graph.movement.walk_graph(g, '__call__')

    return g
