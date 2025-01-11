# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 18:47:58 2022

@author: fs.egb
"""
import pandas as pd


import setup_panel 
import network 

def main_outcomes(panel, y_i, df):
    """ 
    get number of private entities per period
    calculate network
    get network centralities per period
    """
    frames = []
    for y in y_i: 
        print(f"panel {y}")
        temp = df[df['y']<= y]
        sub_p = panel[panel['y'] == y]
        private = ['sociedade por quotas','sociedade individual',
                   'sociedade anonima']
        private_firms = temp[temp['orga_type'].isin(private)]

        all_entitiy_reg, firm_dict = setup_panel.get_owner_reg(private_firms)
        
        length =  {k: len(v) for k,v in  all_entitiy_reg.items()}
        sub_p["private_companies"] = sub_p['id'].map(length)
        G = network.create_undirected_network(all_entitiy_reg, firm_dict)
        centralities = network.collect_centralities(G)
        all_ = sub_p.merge(centralities, left_on = 'id', right_index = True , how = "left")
        
        frames.append(all_)
      
    out_panel = pd.concat(frames)  
    
    return out_panel