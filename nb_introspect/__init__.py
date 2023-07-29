"""
A simple IPython plugin that analyzes and remembers the contents 
of cell docstrings so that the cell contents can be gotten in Python code. 
"""

import ast 

from IPython.core.getipython import get_ipython

from . import cellcache

def get(expr):
    """Get cache entry"""
    return cache.find(expr)

def source(expr):
    return get(expr).info.raw_cell

def tree(expr):
    return ast.parse(get_ipython().transform_cell(source(expr)))

def result(expr):
    return get(expr).result

def run(expr):
    return get_ipython() \
        .run_cell(source(expr), store_history=False, silent=False).result

def load_ipython_extension(ipython):
    global cache
    cache = cellcache.CellCache(ipython)
    ipython.events.register('post_run_cell', cache.post_run_cell)

def unload_ipython_extension(ipython):
    global cache
    cache = None
    ipython.events.unregister('post_run_cell', cache.post_run_cell)

# global singleton
cache = None 
