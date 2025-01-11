# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 16:46:20 2022

@author: fs.egb
"""


def get_owner_per_entry(df):
    """
    Merges the beneficial owner and the previous owner into a single col 
    for each row

    """

    owner_dict = dict(zip( df.index,  df['Beneficial owner']))
    owner_dict = {k:v for k, v in owner_dict.items() if isinstance(v, str)}
    
    
    prev_dict = dict(zip( df.index,  df['Previous_partners']))
    prev_dict = {k: v.replace(";",",") for k,v in prev_dict.items() if isinstance(v, str)}

    prev_share = len(prev_dict )/ len(df)
    print(f"{prev_share:.2%} of the entries list a former owner")
    
    both_dict = {}
    for o in owner_dict:
        if o in prev_dict:
            both_dict[o] = owner_dict[o] +", " + prev_dict[o]   
        if o not in prev_dict:
            both_dict[o] = owner_dict[o]
    
    prev_single = {k: v for k,v in prev_dict.items() if k not in owner_dict}
  
    both_dict.update(prev_single)
    
    df['owner'] = df.index.map(both_dict)
    
    return df
    