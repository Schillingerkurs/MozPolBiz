# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 09:30:31 2022

@author: fs.egb
"""



from pathlib import Path
import numpy as np 
import pandas as pd
import math




def get_matrix_15(HERE)-> dict:
    """ get tables and accouting_matrix from excel sheet"""
    matrx_path = HERE/Path("data","external","social_accounting_matrix")
    matrx_15 = (
                pd.read_excel(matrx_path/
                              Path("2015-Mozambique-SAM-v2018-corrections.xlsx"),
                sheet_name = "2015 Mozambique SAM",  header= 4)
                .replace(0, np.nan)
                .dropna(axis='columns',how='all')
                .dropna(axis='rows',how='all')
                .rename( columns ={'Unnamed: 1':"index_"})
                # .drop_duplicates(subset = ["index_"], keep = "first")
                .set_index('index_')     
                .drop(columns = ['Unnamed: 0', 'col tot', 'diff'])
                .to_dict())
    
    item_tuples = {}
    for k in matrx_15.keys():
        temp = {k: v for k,v in matrx_15[k].items() if not math.isnan(v)}
        for item in temp.keys():
            item_tuples.update({(k,item) : temp[item]})

    N = 5 # the table as a seperate table after N columns
    
    df = pd.read_excel(matrx_path/
            Path("2015-Mozambique-SAM-v2018-corrections.xlsx"),
                sheet_name = "Notes",  header= 9)
    
    labels = np.split(df,
                np.arange(N, len(df.columns), N), axis=1
                )
    
    
    labels =  [x for x in labels if len(x.keys())>0]
    lable_mapper = {}
    for l in labels:
        temp = (l.dropna(how = 'all', axis = 1)
                .dropna(how = 'all', axis = 0))
        if len(temp.keys()) == 2:
            lable_mapper.update(temp.set_index(temp.keys()[0])
                                .iloc[:, 0].to_dict())
        else:
            lable_mapper.update(temp.set_index(temp.keys()[0])
                    .iloc[:, 1].to_dict())
  
            lable_mapper.update(temp.set_index(temp.keys()[1])
                    .iloc[:, 1].to_dict())
    
    out = {}
    out['labels'] = lable_mapper
    out['matrix'] = item_tuples     
    
    return out
    
 
     
    
    
    
    
    
    

        
