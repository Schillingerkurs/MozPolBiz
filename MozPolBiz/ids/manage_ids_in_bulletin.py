# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 12:24:49 2022

@author: fs.egb
"""

import ids

def manage_ids_in_bulletin(df, entity_mapper, level):
    
    
    # df = firms['firmregister_full']
    firm_id_mapper = entity_mapper['bulletin_entities']
     
    name_mapper = entity_mapper['individual_mappings']
       
    df['firm_id'] = df['Companyname'].map(firm_id_mapper)
    
    if level == 'id':
        df = ids.map_owner_ids(df, name_mapper)
    if level == 'family':
        df = ids.map_family_ids(df, name_mapper)
    if level == 'og':
        df == ids.map_og_ids(df, name_mapper)
    df = ids.map_all_owner_ids(df, firm_id = 'firm_id')
    
    return df







