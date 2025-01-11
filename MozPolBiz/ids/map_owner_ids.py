# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 11:47:11 2022

@author: fs.egb
"""

import pandas as pd


import ids






def map_owner_ids(df, name_mapper):
    """
    map owner ids on single row, i.e. only mentions in a particular entry
    
    """
    if isinstance(name_mapper, pd.DataFrame):
        name_mapper = dict (zip(name_mapper['raw'], name_mapper['id']))
    
    df = ids.get_owner_per_entry(df)
    
    both_dict = dict(zip(df.index,df['owner']))
    
    temp  = {k: v.split( ",") for k,v in both_dict.items() if isinstance(v, str)}
    temp  = {k: [x.strip() for x in v if x != ""] for k,v in temp.items()}
    
    doof  = {k: [x for x in v if x not in name_mapper] for k,v in temp.items()}
    doof = {k: v for k,v in doof.items() if v!= []}
    
    print(f"{doof} is missing in the name_mapper ")
    
    temp  = {k: [name_mapper[x] for x in v ] for k,v in temp.items() if k not in doof}
    
    df['owner_ids'] = df.index.map(temp)
    
    df['owner_ids'] =   df['owner_ids'].fillna("")
    
    return df
    