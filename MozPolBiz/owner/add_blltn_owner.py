# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 11:42:26 2022

@author: fs.egb
"""


import owner

def add_blltn_owner(df):
    """ get owners per row in blltn"""
    df = owner.get_owner_per_entry(df)
    owner_dict = dict(zip(df.index, df['owner']))
    owner_dict = {k: v for k, v in owner_dict.items() if isinstance(v,str)}
    owner_dict  = {k: v.split (", ") for k, v in owner_dict.items()}
    owner_dict  = {k: [x.strip() for x in v if x != ""] for k,v in owner_dict.items()}
    return owner_dict
    