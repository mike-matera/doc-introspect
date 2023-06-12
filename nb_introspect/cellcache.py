"""
A class that remembers executed cells. 
"""

import re 
import ast 


class CellCache:

    def __init__(self, ipython):
        self._ipython = ipython
        self._cache = {
            'by-id': {},
            'by-tag': {},
        } 

    def _lookup(self, info):
        """Lookup a cell in the cache."""

        entry = self._cache['by-id'].get(info.cell_id, {
                'info': info,
                'result': None,
            })
        self._cache['by-id'][info.cell_id] = entry

        # Parse the docstring
        tags = []
        try:
            if (doc := ast.get_docstring(ast.parse(self._ipython.transform_cell(info.raw_cell)))) is not None:
                tags = [m.group(1) for x in doc.split('\n') if (m := re.match('(@\S+)', x.strip())) is not None]
        except SyntaxError as e:
            pass 

        for tag in tags:
            self._cache['by-tag'][tag] = entry
        
        return entry 
    
    def find(self, search):
        """Find a cache entry."""
        if search.startswith('@'):
            # find tag
            return self._cache['by-tag'][search]
        else:
            # find ID
            return self._cache['by-id'][search]
        
    def pre_run_cell(self, info):
        self._lookup(info)

    def post_run_cell(self, result):
        entry = self._lookup(result.info)
        entry['result'] = result
