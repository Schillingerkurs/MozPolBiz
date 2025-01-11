# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 14:04:29 2022

@author: fs.egb
"""


from collections import defaultdict

def get_owner_reg(bltn):
    firm_dict = dict(zip(bltn['firm_id'], bltn['all_owner_ids']))
    firm_dict = {k: v.split(", ") for k,v in firm_dict.items()}

    firm_dict = {k: [x for x in v if x != ''] for k,v in firm_dict.items() if v}
    out = []
    for r in list(firm_dict):
         for e in firm_dict[r]:
                out.append((e ,r ))   
                
    d = defaultdict(list)
    for k, v in out:
        d[k].append(v)
        
    d = {k: list(set(v)) for k,v in d.items()}
    return d, firm_dict
