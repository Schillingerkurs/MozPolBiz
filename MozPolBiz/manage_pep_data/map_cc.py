# -*- coding: utf-8 -*-
"""
Created on Fri Apr  1 11:39:27 2022

@author: fs.egb
"""


def map_cc(pep_mandates, name_mapper, panel, y_i): 
    cc = pep_mandates['CC']    
    cc['id'] = cc['name'].map(name_mapper)
      
    years = list(cc['Year_position'].unique())
    years = [ x for x in years if x > min (y_i)]
    product = []
    for n,y in enumerate(years):
        if y < max(years):
            period =  range(y, years[n+1],1)  
        if y == max(years):
            period = range(y, max(y_i),1)                      
        names = cc[cc['Year_position'] == y]['id']
        for ow in names:
            product.extend([(ow,year) for year in period])
            
          
    cc_mapper = {k: 1 for k in product}
    
    panel['cc'] = panel['m'].map(cc_mapper)
  
    
    return panel
    
