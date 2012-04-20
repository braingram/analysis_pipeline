#!/usr/bin/env python
"""
"""

import logging


def load_obj(name):
    if '.' in name:
        i = name.rfind('.')
        module = __import__(name[:i], fromlist=('.' in name[:i]))
        objname = name[i + 1:]
        return getattr(module, objname)
    return eval(name)


def load_class(name, kwargs):
    return load_obj(name)(**kwargs)


def load_function(name):
    return load_obj(name)


def load(cfg, name):
    """
    Load a pipeline operation from a config file

    Parameters
    ----------
    cfg : ConfigParser or cconfig.CConfig etc...
        configuration file that defines the node within a section
        of the same name
    name : str
        name of the node to load and the section within cfg that defines
        the node

    Returns
    -------
    operation : function or class instance
        both are callable, class may have an init function
    kwargs : dict
        keyword arguments for calling the function or class instance
    """
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
        return load_class(ovalue, kwargs), kwargs
    elif otype == 'func':
        return load_function(ovalue), kwargs
    elif otype == 'clone':
        op, kw = load(cfg, ovalue)
        kw.update(kwargs)
        return op, kw
    else:
        raise ValueError("Unknown operation def: %s, %s" % (otype, ovalue))


def parse_node(cfg, node):
    op, kwargs = load(cfg, node)
    return {'op': op, 'kwargs': kwargs}
