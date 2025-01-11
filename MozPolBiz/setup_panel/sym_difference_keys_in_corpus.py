# -*- coding: utf-8 -*-
"""
Created on Mon May 16 12:46:29 2022

@author: fs.egb
"""


import pandas as pd

import setup_panel



def sym_difference_keys_in_corpus(df,panel, y_i, difference):
    """ 
    counts how many entities contain the symmetric difference of keywords
    returns integer
    
    """
    corpus =  dict(zip(df.index, df['corpus_norm']))
    relev_entities =  set()
    
  

    t = [k for k,v in corpus.items() if difference[0] in v and difference[1] not in v ]
    relev_entities.update(t)

    frames = []
    for y in y_i:
        annula_reg = df[df['y']<= y]
        sub_p = panel[panel['y']== y]
        temp  = annula_reg.filter(items = list(relev_entities), axis=0)
        all_entitiy_reg, firm_dict = setup_panel.get_owner_reg(temp)
        length =  {k: len(v) for k,v in  all_entitiy_reg.items()}
        sub_p[f"{difference[0]}_but_not_{difference[1]}"] = sub_p['id'].map(length)
        frames.append(sub_p)
        
    out_panel = pd.concat(frames) 
    out_panel = out_panel.drop(columns = ['id','y'])       
    
    
    return out_panel
        