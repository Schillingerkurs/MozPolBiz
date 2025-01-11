# -*- coding: utf-8 -*-
"""
Created on Tue Aug 23 22:09:41 2022

@author: fs.egb
"""

import pandas as pd

import setup_panel 
import network 
import ids


def get_pre_bonanza_peps(panel_full, y):
    """
    get all PEP (but not Opposition) ids and families names 
    before 2009 (i.e. the discovery)
    """
     
    df = panel_full[panel_full['y'] <= y]
    df = df.loc[(df["Minister"] == 1) 
                |(df["Governor"] == 1) 
                |(df["Minister_who_gov"] == 1)
                |(df["MP"] == 1)
                |(df["cc"] == 1)
                |(df["pb"] == 1)
                ]
    
    
    pre_PEP = set(df['id'])
    pre_PEP_families = dict(df
                        .drop_duplicates(subset = ["id"])
                        ['family'].value_counts())
                  
    return pre_PEP_families, pre_PEP





def pep_affil_bnz(panel_full, firms, entity_mapper):
    """ 
    count how many direct business partners are pre 2009 PEPs.
    
    """
    
    y = 2009 
    
    firms = ids.manage_ids_in_bulletin(firms, entity_mapper, level = 'id')
    
    
    pre_PEP_families, pre_PEP = get_pre_bonanza_peps(panel_full, y)
    

    print(f"panel {y}")
    pre_bonaza_firms = firms[firms['y']<= y]
    

    all_entitiy_reg, firm_dict = setup_panel.get_owner_reg(pre_bonaza_firms)
    
    G = network.create_undirected_network(all_entitiy_reg, firm_dict)
    
    pep_counter = {}
    for nodes in G.nodes:
        pep_partner = pre_PEP.intersection(set(G.neighbors(nodes)))
        pep_counter[nodes] = len(pep_partner)
            
        
    panel_full['family_old_peps'] = panel_full['family'].map(pre_PEP_families)
    panel_full['old_pep_business'] = panel_full['id'].map(pep_counter)       
    
    
    return panel_full
        
        