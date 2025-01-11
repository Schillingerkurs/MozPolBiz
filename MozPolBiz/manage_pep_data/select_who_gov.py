# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 19:45:23 2022

@author: fs.egb
"""


def select_who_gov(pep_mandates, name_mapper, panel): 
    who_gov = pep_mandates['Who_Gov']   
    
    who_gov = who_gov[~who_gov['name'].isna()]
    
    who_gov['id'] = who_gov['name'].map(name_mapper)
      
    who_gov["m"] = who_gov[["id","year"]].apply(tuple, axis=1)    
    mnstr = dict(zip(who_gov['m'], who_gov['minister']))
    # core =  dict(zip(who_gov['m'], who_gov['core']))
    
    panel['Minister_who_gov'] = panel['m'].map(mnstr)
    
    
    return panel
    