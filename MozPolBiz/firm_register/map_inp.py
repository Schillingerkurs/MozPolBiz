# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 16:28:12 2022

@author: fs.egb
"""

import pandas as pd
from string_grouper import match_strings
import numpy as np


import firm_register as f_r



def map_inp(investing_firms,keywrds, entity_mapper):
    
    
    inp = keywrds.parse('inp')
    inp_shareholder_dict = dict(zip(inp['Name'], inp['shareholders']))
    inp_shareholder_dict = {k:v.split("+")  for k,v in inp_shareholder_dict.items()}
    inp_only_names = {k: [f_r.norm_firm_names(x) for x in v] for k,v in 
                      inp_shareholder_dict.items()}

    all_names = set()
    for a in inp_only_names:
        for f in inp_only_names[a]:
            all_names.add(f)         
    aff_field = {}        
    for e in all_names:
        aff_field[e] = ", ".join([k for k,v in inp_only_names.items() if e in v])
       
    gas_shareholders = pd.Series(aff_field.keys())
    
    fdi_mapp = pd.Series({k: f_r.norm_firm_names(k) for 
                          k in investing_firms})
    
    # controlled all matches by hand -> even 46 % is ok.
    treshold = 0.46
    m = match_strings(gas_shareholders,  fdi_mapp, min_similarity = treshold)

    gas_shareholders_map  = dict(zip(m['left_side'], m['right_index']))
    
    gas_shareholders = pd.DataFrame(gas_shareholders, columns = ['norm_n'])
    gas_shareholders['FDI_link'] = gas_shareholders['norm_n'].map(gas_shareholders_map)
                                 
    treshold = 0.818
    blltn_map = pd.Series(entity_mapper['corpus'])
    
    m = match_strings(gas_shareholders['norm_n'],  blltn_map, min_similarity = treshold)
    
    
    gas_entities_map  = dict(m.groupby('left_norm_n')['right_index'].apply(lambda x: list(np.unique(x))))
    gas_entities_map  = {k: [entity_mapper['all_entity_mapper'][x]
                           for x in v] for k,v in gas_entities_map.items()}
    
    gas_entities_map  = {k: [str(x) for x in v] for k,v in gas_entities_map.items()}
    
    gas_entities_map  = {k: ", ".join(v) for k,v in gas_entities_map.items()}

    gas_shareholders['bltn_link'] = gas_shareholders['norm_n'].map(gas_entities_map)
    

    hand_matches = keywrds.parse('inp_flexi_hand_match')
    
    mapy = dict(zip(hand_matches['inp_norm'],hand_matches['Full_name']))
    
    
    gas_shareholders['hand_match'] = gas_shareholders['norm_n'].map(mapy)
    
    gas_shareholders['affi_gas_fields'] = gas_shareholders['norm_n'].map(aff_field)
    
    return gas_shareholders


    