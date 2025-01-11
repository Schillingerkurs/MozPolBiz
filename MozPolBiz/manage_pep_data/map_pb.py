# -*- coding: utf-8 -*-
"""
Created on Sun Apr  3 12:08:59 2022

@author: fs.egb
"""

def map_pb(pep_mandates, name_mapper, panel, y_i): 
    pb = pep_mandates['polit_bureau']    
    pb['id'] = pb['name'].map(name_mapper)
      
    years = list(pb['Year_position'].unique())
    years = [ x for x in years if x > min (y_i)]
    product = []
    for n,y in enumerate(years):
        if y < max(years):
            period =  range(y, years[n+1],1)  
        if y == max(years):
            period = range(y, max(y_i),1)                      
        names = pb[pb['Year_position'] == y]['id']
        for ow in names:
            product.extend([(ow,year) for year in period])
            
          
    pb_mapper = {k: 1 for k in product}
    
    panel['pb'] = panel['m'].map(pb_mapper)
  
    
    return panel
    