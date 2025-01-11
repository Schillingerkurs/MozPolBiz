# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 13:13:30 2022

@author: fs.egb
"""
import pandas as pd

import setup_panel
import dbwho_specs



def count_dbwho_industries(df,panel, y_i):
    df_adjust  = dbwho_specs.adjust_dbwho_ist(df)
    frames = []
    for y in y_i:
        annula_reg = df_adjust[df_adjust['y']<= y]
        sub_p = panel[panel['y']== y]
        for orga in ['finance','trading',"BusinessServices","Transport","Health/Education",
                     'Construction','Heavy industry & mining', "other","unclassified","Commerce"]:
            temp = annula_reg[annula_reg['industry_primary']== orga]
            all_entitiy_reg, firm_dict = setup_panel.get_owner_reg(temp)
            length =  {k: len(v) for k,v in  all_entitiy_reg.items()}
            sub_p[orga] = sub_p['id'].map(length)
            
        frames.append(sub_p)
           
    out_panel = pd.concat(frames)      
    out_panel = out_panel.drop(columns = ['id','y'])
    
    return out_panel
