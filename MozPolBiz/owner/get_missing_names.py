# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 11:24:50 2022

@author: fs.egb
"""

def get_missing_names(all_names, base):
    missing_names = set(all_names)-set(base['raw'])
    for m in missing_names:
        dict_ = {'raw':m ,'family': '', 'beta_clean':'', 'gender':0.5, 'id':'', 'lawyer':''}
        base = base.append(dict_, ignore_index = True)
        
    return base