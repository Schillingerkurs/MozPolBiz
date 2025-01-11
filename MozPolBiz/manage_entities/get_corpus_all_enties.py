# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 11:27:43 2022

@author: fs.egb
"""
import firm_register



def get_corpus_all_enties(entity_mapper= dict()) -> dict:
    t = list()
    for k in entity_mapper:
        t.extend(entity_mapper[k])
    
    corpus = firm_register.dict_norm(t)
    return  corpus