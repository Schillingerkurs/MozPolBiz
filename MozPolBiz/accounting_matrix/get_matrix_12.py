# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 12:57:06 2022

@author: fs.egb
"""


from pathlib import Path
import numpy as np 
import pandas as pd
import math




def get_actual_matrix(matrx_path):
    matrx_12 = (
                pd.read_excel(matrx_path/
                              Path("Data for a 2012 SAM for Mozambique.xlsx"),
                sheet_name = "Consolidated balanced STDSAM")
              
                .replace(0, np.nan)
                .dropna(axis='columns',how='all')
                .dropna(axis='rows',how='all')
                .rename( columns ={'Unnamed: 1':"index_"})
                .drop_duplicates(subset = ["index_"], keep = "first")
                .set_index('index_')     
                )
            
    matrx_12.columns = matrx_12.iloc[0]
    
    matrix_mapper = (
        matrx_12[matrx_12.index.notnull()]
        .drop(columns = ['total','col tot', 'diff'])
        .to_dict())
    
    item_tuples = {}
    for k in matrix_mapper.keys():
        temp = {k: v for k,v in matrix_mapper[k].items() if not math.isnan(v)}
        for item in temp.keys():
            item_tuples.update({(k,item) : temp[item]})
            
    return item_tuples
            
        


def get_matrix_12(HERE)-> dict :
    """ get tables and accouting_matrix from excel sheet"""
    
    
    matrx_path = HERE/Path("data","external","social_accounting_matrix")
    
    matrx_12 = {}
    
    matrx_12['table_1'] =  (
               pd.read_excel(matrx_path/
                             Path("Data for a 2012 SAM for Mozambique.xlsx"),
               sheet_name = "Tables to Doc1", header= 1)
               .rename( columns ={'Unnamed: 1':"index_"})
               .drop_duplicates(subset = ["index_"], keep = "first")
               .set_index('index_')   
               .drop(columns = ["sumif",'Unnamed: 12'])
               )
    
    matrx_12['table_2'] =  (
    pd.read_excel(matrx_path/
          Path("Data for a 2012 SAM for Mozambique.xlsx"),
    sheet_name = "Tables to Doc2", header= 1)
    .rename( columns ={'Unnamed: 1':"index_"})
    .drop_duplicates(subset = ["index_"], keep = "first")
    .set_index('index_')   
    .drop(columns = ["sumif",'Unnamed: 9'])
    )
    
    
    matrx_12['table_3'] =  (
    pd.read_excel(matrx_path/
      Path("Data for a 2012 SAM for Mozambique.xlsx"),
    sheet_name = "Tables to Doc3", header= 1)
    .rename( columns ={'Unnamed: 1':"index_"})
    .drop_duplicates(subset = ["index_"], keep = "first")
    .set_index('index_')   
    .drop(columns = ["sumif",'Unnamed: 16'])
    )
    
    
    
    
    code_mapper = {}
    for m in matrx_12.keys():
        t = matrx_12[m]
        code_mapper.update(t.iloc[:, 0].to_dict())
        
    matrx_12['code_mapper']  = {k:v for k,v in code_mapper.items() if isinstance(v, str)}  
    # map the actual matrix in dict
    matrx_12['matrix'] = get_actual_matrix(matrx_path)
    
    
    
    N = 27 # the table as a seperate table after 26 columns
    df = pd.read_excel(matrx_path/
                       Path("Data for a 2012 SAM for Mozambique.xlsx"),
                       sheet_name = "Tables to Doc4", header= 1)
    multip_table =  np.split(df, np.arange(N, len(df.columns), N), axis=1)
    
    
    matrx_12['table_4'] = multip_table[0]


      
    t_1 =  multip_table[1]
    t_1.columns = t_1.iloc[0]
    t_1 = t_1.dropna(axis='rows',how='all')
    t_2 =  multip_table[2]
    t_2.columns = t_2.iloc[0]
    t_2 = t_2.dropna(axis='rows',how='all')
    
    matrx_12['table_5'] = t_1.merge(t_2, right_index = True, left_index = True)
    
    
    return matrx_12
    