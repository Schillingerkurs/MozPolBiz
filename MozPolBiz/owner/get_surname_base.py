# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 12:09:36 2022

@author: fs.egb
"""
import owner


def get_surname_base(all_names, family_fuzz):

   
    base = owner.fuzz_map_surnames(all_names = all_names, 
                  family_fuzz = family_fuzz)
    
    
    new_name = base[base['family'] != base['family_beta']]
    new_name = dict(zip(new_name['family'], new_name['family_beta']))
    
    for n in new_name:
        base['clean'] =  base['clean'].str.replace(n, new_name[n])
        
    return base 
