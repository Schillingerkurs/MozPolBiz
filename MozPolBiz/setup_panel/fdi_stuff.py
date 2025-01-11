# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 10:43:13 2022

@author: fs.egb
"""
# from collections import Counter

import pandas as pd

import setup_panel


def count_fdi_affiliations(df,panel, y_i):
    """ 
    count number of firms that are affilaited with fdi via institutional 
    ownership
    """
    frames = []
    for y in y_i:
        annula_reg = df[df['y']<= y]
        sub_p = panel[panel['y']== y]
        temp = annula_reg[annula_reg['fdi_shareholder']== 1]
        all_entitiy_reg, firm_dict = setup_panel.get_owner_reg(temp)
        length =  {k: len(v) for k,v in  all_entitiy_reg.items()}
        sub_p['fdi_affiliates'] = sub_p['id'].map(length)
        
        frames.append(sub_p)
           
    out_panel = pd.concat(frames)      
    out_panel = out_panel.drop(columns = ['id','y'])
    
    return out_panel


def count_fdis(df,panel, y_i):
    """
    count firms that are direct FDIs.
    """

    frames = []
    for y in y_i:
        annula_reg = df[df['y']<= y]
        sub_p = panel[panel['y']== y]
        temp = annula_reg[~annula_reg['fdi_firm'].isna()]
        all_entitiy_reg, firm_dict = setup_panel.get_owner_reg(temp)
        length =  {k: len(v) for k,v in  all_entitiy_reg.items()}
        sub_p['fdi_owner'] = sub_p['id'].map(length)
        
        frames.append(sub_p)
           
    out_panel = pd.concat(frames)      
    out_panel = out_panel.drop(columns = ['id','y'])
    
    return out_panel




    
    
   