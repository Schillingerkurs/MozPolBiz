# -*- coding: utf-8 -*-
"""
Created on Mon May 16 07:35:49 2022

@author: fs.egb
"""

    
import pandas as pd

import setup_panel




def count_key_in_corpus(df,panel, y_i, keyword_dict):
    """ 
    counts how many entities contain a list of keywords
    returns integer
    
    """
    
    keyword_list = [f for s in list(keyword_dict.values()) for f in s]
    corpus =  dict(zip(df.index, df['corpus_norm']))
    relev_entities =  set()
    
    for key in keyword_list:
        t = [k for k,v in corpus.items() if key in v]
        relev_entities.update(t)

    frames = []
    for y in y_i:
        annula_reg = df[df['y']<= y]
        sub_p = panel[panel['y']== y]
        temp  = annula_reg.filter(items = list(relev_entities), axis=0)
        all_entitiy_reg, firm_dict = setup_panel.get_owner_reg(temp)
        length =  {k: len(v) for k,v in  all_entitiy_reg.items()}
        sub_p[f"{list(keyword_dict.keys())[0]}_industry"] = sub_p['id'].map(length)
        frames.append(sub_p)
        
    out_panel = pd.concat(frames) 
    out_panel = out_panel.drop(columns = ['id','y'])       
    
    
    return out_panel
        




