# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 18:31:04 2022

@author: fs.egb
"""


def dwbho_cntr_vars(df, panel, y_i):
    frames = []
    for y in y_i:
        temp = df[df['y']<= y]
        sub_p = panel[panel['y']== y]
        for orga in ['registration','alteration',"closure"]:
            all_entitiy_reg, firm_dict = setup_panel.get_owner_reg(temp[temp['annoucment']== orga])
            length =  {k: len(v) for k,v in  all_entitiy_reg.items()}
            sub_p[orga] = sub_p['id'].map(length)
            
        frames.append(sub_p)
                     
    panel = pd.concat(frames)  
    panel = panel.drop(columns = ['id','y'])
    return panel

