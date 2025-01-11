# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 18:45:58 2022

@author: fs.egb
"""

import pandas as pd


import setup_panel


def cntr_vars(df, panel, y_i):
    """
    Count 
    'sociedade cooperativa',
    'representacao comercial',
    "fundacao",
    "associacao"
    
    per person.

    """
    frames = []
    for y in y_i:
        temp = df[df['y']<= y]
        sub_p = panel[panel['y']== y]
        for orga in ['sociedade cooperativa','representacao comercial',"fundacao","associacao"]:
            all_entitiy_reg, firm_dict = setup_panel.get_owner_reg(temp[temp['orga_type']== orga])
            length =  {k: len(v) for k,v in  all_entitiy_reg.items()}
            sub_p[orga] = sub_p['id'].map(length)
            
        frames.append(sub_p)
                     
    panel = pd.concat(frames)  
    panel = panel.drop(columns = ['id','y'])
    return panel