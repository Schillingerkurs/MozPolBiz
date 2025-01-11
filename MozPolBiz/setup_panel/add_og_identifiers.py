# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 18:28:53 2022

@author: fs.egb
"""

def add_og_identifiers(firms):
    
    name_mapper  = firms['entity_name_mapper']['individual_mappings']
    df = firms['firmregister_full']

    entity_mapper = firms['entity_name_mapper']
    

    df = ids.manage_ids_in_bulletin(df, entity_mapper, 'individual')

    og_mapper  = network.get_og_network(blltn = df ,
                                        og_year = 1990)
    
    name_mapper['og'] = name_mapper['id'].map(og_mapper) 
    name_mapper['og'] = name_mapper['og'].fillna(name_mapper['id'])


    firms['entity_name_mapper']['individual_mappings'] = name_mapper    
    
    return firms