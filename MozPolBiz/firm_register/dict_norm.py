# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 19:49:40 2022

@author: fs.egb
"""
import firm_register


def dict_norm(indict = dict()) -> dict:
    """ norms the strings values in a dict"""
    corpus = {k:firm_register.norm_firm_names(k) for k in indict}
    corpus = {k:firm_register.lemmatizing_entity_names(v) for k,v in corpus.items()}
    corpus = {k:firm_register.remove_orga_string(v) for k,v in corpus.items()}  
    return corpus

