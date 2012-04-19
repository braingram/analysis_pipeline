#!/usr/bin/env python

import pylab

import networkx
import networkx.readwrite

import cconfig


class Debug(object):
    def __init__(self, **kwargs):
        print "Debug(%s).__init__: %s" % (id(self), kwargs)

    def init(self, graph, **kwargs):
        print "Debug(%s).init: %s" % (id(self), graph)

    def __call__(self, *args, **kwargs):
        print "Debug(%s).run: %s" % (id(self), args)


def debug(*args, **kwargs):
    print "debug: %s %s" % (args, kwargs)


def load_operation(cfg, name):
    if name not in cfg.sections():
        return lambda *args: args, {}
    kwargs = dict([(k, v) for k, v in cfg.items(name) if k[0] != '_'])
    control = [(k[1:], v) for k, v in cfg.items(name) if k[0] == '_']
    if len(control) != 1:
        raise ValueError("Invalid control options for %s: %s" % \
                (name, control))
    else:
        otype, ovalue = control[0]
    if otype == 'class':
        return eval(ovalue)(**kwargs), kwargs
    elif otype == 'func':
        return eval(ovalue), kwargs
    elif otype == 'clone':
        op, kw = load_operation(cfg, ovalue)
        kw.update(kwargs)
        return op, kw
    else:
        raise ValueError("Unknown operation def: %s, %s" % (otype, ovalue))


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
        print "Found start node: %s" % cursor
    if cursor not in run_nodes:
        if not (all([pn in run_nodes for pn in graph.predecessors(cursor)])):
            # do not attempt to run node before all predecessors have run
            # since not all preds are run, this should get called again
            # so just jump out for now
            print "skipping call %s on %s" % (func, cursor)
            return
        else:
            print "calling %s on %s" % (func, cursor)
            op = graph.node[cursor]['op']
            if len(args) == 0:
                # get args from predecessors
                args = [graph.node[pn]['result'] for pn \
                        in graph.predecessors(cursor)]
            if hasattr(op, func):
                graph.node[cursor]['result'] = getattr(op, func)(*args, \
                        **graph.node[cursor]['kwargs'])
            run_nodes.append(cursor)
    print "walking to successors of %s: %s" % \
            (cursor, graph.successors(cursor))
    for node in graph.successors(cursor):
        walk_graph(graph, func, node, run_nodes, args)
    if 'result' in graph.node[cursor]:
        graph.node[cursor].pop('result')


def parse_node(cfg, node):
    op, kwargs = load_operation(cfg, node)
    return {'op': op, 'kwargs': kwargs}


def run_pipeline(cfgfile):
    cfg = cconfig.TypedConfig(local=cfgfile)
    graph = networkx.readwrite.read_edgelist(cfg.get('pipeline', 'graph'), \
            create_using=networkx.DiGraph())
    #graph = networkx.readwrite.read_edgelist(cfg.get('pipeline', 'graph'), \
    #        nodetype=Node, create_using=networkx.DiGraph())

    print "Start node:", find_start(graph)

    print "====== PARSE ======="
    for node in graph.nodes_iter():
        print "parsing node: %s" % node
        graph.node[node] = parse_node(cfg, node)

    print "====== INIT ======="
    walk_graph(graph, 'init', args=[graph, ])

    print "====== RUN ======="
    walk_graph(graph, '__call__')

    #networkx.draw(graph)
    #pylab.show()

    return graph

if __name__ == '__main__':
    run_pipeline('graph.ini')
