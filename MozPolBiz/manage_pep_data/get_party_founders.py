# -*- coding: utf-8 -*-
"""
Created on Mon May 16 10:54:00 2022

@author: fs.egb
"""

import pandas as pd


import ids
import setup_panel

def get_party_founders(panel, firms, y_i, entity_mapper):

    """
    creates dummy in the year a person founded a party
    """
    df = firms[firms['orga_type'] == 'partido politico']
    
    
    df = ids.manage_ids_in_bulletin(df, entity_mapper, level = 'id')
       
    parties = (
        firms[firms['orga_type']== "partido politico"]
        .set_index('firm_id')['Companyname']
        .to_dict()       
            )

    all_entitiy_reg, firm_dict = setup_panel.get_owner_reg(df)
    
    frames = []
    for y in y_i:
        annula_reg = df[df['y']== y]
        sub_p = panel[panel['y']== y]
        all_entitiy_reg, firm_dict = setup_panel.get_owner_reg(annula_reg)
        length =  {k: v for k,v in  all_entitiy_reg.items()}
        sub_p['party_founder'] = sub_p['id'].map(length)
        
        frames.append(sub_p)
           
    out_panel = pd.concat(frames)      
    out_panel = out_panel.drop(columns = ['id','y'])
    
    founder_mapper = dict(zip(out_panel['m'], out_panel['party_founder']))
    
    founder_mapper = {k: parties[v[0]] for k,v in founder_mapper.items() \
                      if not isinstance(v,float)}
    
    
    return founder_mapper

