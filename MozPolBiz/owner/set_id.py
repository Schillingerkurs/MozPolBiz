# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 10:49:44 2022

@author: fs.egb
"""


def set_id(input_list, pre_tag):
    """ 
    input_list -> list of strings 
    
    out: mapper with IDS
    
    replace unique names with id.
    id contains date of creation.
    
    """
    out = {}
    for counter,k in enumerate(input_list): 
        out[k]   = f"{pre_tag}_{counter}"
    return out
