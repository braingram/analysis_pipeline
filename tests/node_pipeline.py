#!/usr/bin/env python

import pylab

import networkx
import networkx.readwrite

import cconfig


class Debug(object):
    def __init__(self, **kwargs):
        print "Debug(%s).__init__: %s" % (id(self), kwargs)

    def init(self, graph):
        print "Debug(%s).init: %s" % (id(self), graph)

    def run(self, *args):
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
        return op, kw.update(kwargs)
    else:
        raise ValueError("Unknown operation def: %s, %s" % (otype, ovalue))


class Node(object):
    def __init__(self, name):
        self.name = name
        self.operation = None
        self.kwargs = None

    def parse(self, cfg):
        self.operation, self.kwargs = load_operation(cfg, self.name)

    def init(self, graph):
        if hasattr(self.operation, 'init'):
            getattr(self.operation, 'init')(graph)

    def run(self, *args):
        if hasattr(self.operation, 'run'):
            getattr(self.operation, 'run')(*args)
        elif hasattr(self.operation, '__call__'):
            self.operation(*args, **self.kwargs)
        else:
            raise AttributeError("Operation %s contains no run or __call__ " \
                    "attribute: %s" % (self.name, self))

    def __hash__(self):
        return self.name.__hash__()

    def __eq__(self, other):
        return self.name.__eq__(other)

    #def __cmp__(self, other):
    #    return self.name.__cmp__(other)

    def __repr__(self):
        return repr(self.name)

    def __str__(self):
        return self.name


def find_start(graph):
    """
    return the first graph node with no predecessors
    """
    for node in graph.nodes_iter():
        if len(graph.predecessors(node)) == 0:
            return node


def walk_graph(graph, func, cursor=None, run_nodes=[], args=[], kwargs={}):
    if cursor is None:
        cursor = find_start(graph)
        print "Found start node: %s" % cursor.name
    if cursor not in run_nodes:
        if not (all([pn in run_nodes for pn in graph.predecessors(cursor)])):
            # do not attempt to run node before all predecessors have run
            # since not all preds are run, this should get called again
            # so just jump out for now
            print "skipping call %s on %s" % (func, cursor.name)
            return
        else:
            print "calling %s on %s" % (func, cursor.name)
            if len(kwargs) and len(args):
                getattr(cursor, func)(*args, **kwargs)
            elif len(args):
                getattr(cursor, func)(*args)
            elif len(kwargs):
                getattr(cursor, func)(**kwargs)
            else:
                getattr(cursor, func)()
            run_nodes.append(cursor)
    print "walking to successors of %s: %s" % \
            (cursor.name, graph.successors(cursor))
    for node in graph.successors(cursor):
        walk_graph(graph, func, node, run_nodes, args, kwargs)


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
        node.parse(cfg)

    print "====== INIT ======="
    walk_graph(graph, 'init', args=[graph, ])

    print "====== RUN ======="
    walk_graph(graph, 'run')

    networkx.draw(graph)

if __name__ == '__main__':
    run_pipeline('graph.ini')
