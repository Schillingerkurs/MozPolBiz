# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 13:11:13 2022

@author: fs.egb
"""


import setup_panel
def first_firm(full_panel, df):
    """
    get year when the firm was registered
    """
    private = ['sociedade por quotas','sociedade individual',
               'sociedade anonima']
    private_firms = df[df['orga_type'].isin(private)]

    first_entity_y = dict(private_firms.groupby('firm_id')['y'].min())
    all_entitiy_reg, firm_dict = setup_panel.get_owner_reg(private_firms)
    
    first_reg = {k: min([first_entity_y[x] for x in v]) for k,v in all_entitiy_reg.items()}
    
    full_panel['first_firm'] = full_panel['id'].map(first_reg)
    
    return full_panel