# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 14:56:51 2022

@author: fs.egb
"""
import pandas as pd

import setup_panel
import network


def firms_without_fdi(panel, df,y_i):
    no_fdi = df[df['fdi_firm'].isna()]
    no_fdi = no_fdi[no_fdi['fdi_shareholder'].isna()]
    difference = len(df) -len(no_fdi)
    
    print(f"Drop {difference} firms with some sort of FDI affiliation")
    
    frames = []
    for y in y_i: 
        print(f"panel {y}")
        temp = no_fdi[no_fdi['y']<= y]
        sub_p = panel[panel['y']== y]

        all_entitiy_reg, firm_dict = setup_panel.get_owner_reg(temp)
        
        length =  {k: len(v) for k,v in  all_entitiy_reg.items()}
        sub_p["private_companies"] = sub_p['id'].map(length)
        G = network.create_undirected_network(all_entitiy_reg, firm_dict)
        centralities = network.collect_centralities(G)
        all_ = sub_p.merge(centralities, left_on = 'id', right_index = True , how = "left")
        frames.append(all_)

        
    out_panel = pd.concat(frames)  
    
    return out_panel
