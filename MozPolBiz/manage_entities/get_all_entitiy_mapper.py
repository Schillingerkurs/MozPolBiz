# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 11:26:10 2022

@author: fs.egb
"""

def get_all_entitiy_mapper(entity_mapper):
    
    all_entity_mapper = {}
    for k in entity_mapper:
        if k not in ['all_entity_mapper', 'corpus']:
            all_entity_mapper.update(entity_mapper[k])
        else:
            continue
    
    entity_mapper['all_entity_mapper'] = all_entity_mapper
    
    return entity_mapper
