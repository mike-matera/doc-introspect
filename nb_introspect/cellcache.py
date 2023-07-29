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
    
    def find(self, search):
        """Find a cache entry."""
        if search.startswith('@'):
            # find tag
            return self._cache['by-tag'][search]
        else:
            # find ID
            return self._cache['by-id'][search]
        
    def post_run_cell(self, result):
        self._cache['by-id'][result.info.cell_id] = result

        # Parse the docstring
        tags = []
        try:
            if (doc := ast.get_docstring(ast.parse(self._ipython.transform_cell(result.info.raw_cell)))) is not None:
                tags = [m.group(1) for x in doc.split('\n') if (m := re.match('(@\S+)', x.strip())) is not None]
        except SyntaxError as e:
            pass 

        for tag in tags:
            print("Found tag:", tag)
            self._cache['by-tag'][tag] = result
        