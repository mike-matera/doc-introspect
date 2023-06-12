"""
A simple IPython plugin that analyzes and remembers the contents 
of cell docstrings so that the cell contents can be gotten in Python code. 
"""

from . import cellcache

def get(expr):
    """Get cache entry"""
    return cache.find(expr)

def source(expr):
    return get(expr)['info'].raw_cell

def result(expr):
    return get(expr)['result'].result

def load_ipython_extension(ipython):
    global cache
    cache = cellcache.CellCache(ipython)
    ipython.events.register('pre_run_cell', cache.pre_run_cell)
    ipython.events.register('post_run_cell', cache.post_run_cell)

def unload_ipython_extension(ipython):
    global cache
    ipython.events.unregister('pre_run_cell', cache.pre_run_cell)
    ipython.events.unregister('post_run_cell', cache.post_run_cell)

# global singleton
cache = None 
