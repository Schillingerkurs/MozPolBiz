# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 20:13:34 2022

@author: fs.egb
"""

def map_mps(pep_mandates,name_mapper, panel):
    mps = pep_mandates['MPs']
    mps['id'] = mps['name'].map(name_mapper)
    
    product = []
    for y in  mps['Year_position'].unique():
        names = mps[mps['Year_position'] == y]['id']
        period = range(y, y+5,1)
        for ow in names:
            product.extend([(ow,year) for year in period])
    
    mp_mapper = {k: 1 for k in product}
    
    panel['MP'] = panel['m'].map(mp_mapper)
    
    return panel
        