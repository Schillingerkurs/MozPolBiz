# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 20:01:20 2022

@author: fs.egb
"""


from pathlib import Path
# import re
import pandas as pd
# import json
pd.options.mode.chained_assignment = None  # default='warn'
import pickle
# import itertools

# import owner
# import manage_pep_data




def dbwho_missing_cols(full_panel, HERE):

    d = HERE/Path("data", "raw","stata_export")
    temp = pd.ExcelFile(d/Path("description_vars.xlsx")).parse("dbwho_var_names")
    
    temp['replace'] = temp['replace'].apply(lambda x: str(x).strip())
    temp['variable_name'] = temp['variable_name'].apply(lambda x: str(x).strip())
      
      
    col_mapper = dict(zip(temp['replace'], temp['variable_name']))
    col_mapper = {k: v for k,v in col_mapper.items() if k!= 'nan'}
    
    full_panel = full_panel.rename(columns  = col_mapper)
    
    
    cols = [x for x in temp['variable_name']]
    
    # missing = [x for x in cols  if x not in full_panel.keys() ]
    
    
    # leftover = [x for x in full_panel.keys()  if x not in cols]
    
    return full_panel