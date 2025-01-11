# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 09:29:27 2022

@author: fs.egb
"""
import networkx as nx


import network


from collections import  defaultdict

def get_owner_reg(df):
    """ 
    transpose
     from: firm1 -> owner 1, owner 2 
     
    
    to: owner 1 - > firm 1, firm 2 ...
    """
    firm_dict = dict(zip(df['firm_id'], df['all_owner_ids']))
    firm_dict = {k: v.split(", ") for k,v in firm_dict.items()}

    firm_dict = {k: [x for x in v if x != ''] for k,v in firm_dict.items() if v}
    out = []
    for r in list(firm_dict):
         for e in firm_dict[r]:
                out.append((e ,r ))   
                
                
                
    d = defaultdict(list)
    for k, v in out:
        d[k].append(v)
        
    entitiy_reg = {k: list(set(v)) for k,v in d.items()}
    
    
    return entitiy_reg, firm_dict


def get_og_network(blltn, og_year):
    df = blltn[blltn['y']<= og_year]
    all_entitiy_reg, firm_dict = get_owner_reg(df)
    G = network.create_undirected_network(all_entitiy_reg, firm_dict)
    
    og_dict = {}
    og_l = list(nx.connected_components(G))
    for coutner,i in enumerate(og_l):
        for s in i:
            og_dict[s]= f"og_{og_year}_{coutner}"
            
    return og_dict
       
        
        