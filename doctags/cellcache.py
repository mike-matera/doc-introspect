"""
A class that remembers executed cells. 
"""

import re 
import ast 

from IPython.core.getipython import get_ipython

class CacheEntry:
    """
    Information about an executed cell. 
    """

    def __init__(self, result):
        """Create an entry."""

        self.id = result.info.cell_id
        self.info = result.info
        self.result = result
        self.source = get_ipython().transform_cell(result.info.raw_cell)

        try:
            self.tree = ast.parse(self.source)
            self.docstring = ast.get_docstring(self.tree)

        except SyntaxError as e:
            self.tree = None
            self.docstring = None

        if self.docstring is not None:
            self.tags = [m.group(1) for x in self.docstring.split('\n') if (m := re.match('(@\S+)', x.strip())) is not None]
        else:
            self.tags = []

class CellCache:
    """
    A cache of cell executions
    """

    def __init__(self):
        self._cache = {
            'by-id': {},
            'by-tag': {},
        } 
    
    def find(self, search):
        """Find a cache entry."""
        if search.startswith('@'):
            # find tag
            return self._cache['by-tag'][search]
        else:
            # find ID
            return self._cache['by-id'][search]
        
    def post_run_cell(self, result):
        entry = CacheEntry(result)        
        self._cache['by-id'][entry.id] = entry
        for tag in entry.tags:
            self._cache['by-tag'][tag] = entry

        