#!/usr/bin/env python

import logging


def find_start(graph):
    """
    return the first graph node with no predecessors
    """
    for node in graph.nodes_iter():
        if len(graph.predecessors(node)) == 0:
            return node


def walk_graph(graph, func, cursor=None, run_nodes=None, args=[]):
    """
    args overrides using predecessor results
    """
    if run_nodes is None:
        run_nodes = []
    if cursor is None:
        cursor = find_start(graph)
        logging.debug("Found start node: %s" % cursor)
    if cursor not in run_nodes:
        if not (all([pn in run_nodes for pn in graph.predecessors(cursor)])):
            # do not attempt to run node before all predecessors have run
            # since not all preds are run, this should get called again
            # so just jump out for now
            logging.debug("skipping call %s on %s" % (func, cursor))
            return
        else:
            logging.debug("calling %s on %s" % (func, cursor))
            op = graph.node[cursor]['op']
            if len(args) == 0:
                # get args from predecessors
                args = [graph.node[pn]['result'] for pn \
                        in graph.predecessors(cursor)]
            if hasattr(op, func):
                graph.node[cursor]['result'] = getattr(op, func)(*args, \
                        **graph.node[cursor]['kwargs'])
            run_nodes.append(cursor)
    logging.debug("walking to successors of %s: %s" % \
            (cursor, graph.successors(cursor)))
    for node in graph.successors(cursor):
        walk_graph(graph, func, node, run_nodes, args)
    if 'result' in graph.node[cursor]:
        graph.node[cursor].pop('result')
