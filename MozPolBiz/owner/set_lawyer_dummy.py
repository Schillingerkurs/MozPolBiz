# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 12:18:05 2022

@author: fs.egb
"""

def set_lawyer_dummy(base, other):
    name_mapper = dict(zip(base['raw'],base['id']))
    lawy = {name_mapper[k]: 1 for k in other['lawyer']['full_name'] if k in name_mapper }
    
    base['lawyer'] = base['id'].map(lawy)
    
    return base
