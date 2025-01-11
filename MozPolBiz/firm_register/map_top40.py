# -*- coding: utf-8 -*-
"""
Created on Fri Sep 17 11:05:51 2021

@author: fs.egb


MAP top 40
"""



import re
from unidecode import unidecode
import pandas as pd
# own module
import firm_register as f_r
from string_grouper import match_strings
import numpy as np


       
def get_blltn_firms(x, corpus_dict, blltn):
        string_clean = unidecode(x.lower())
        fidnigns_dict =  {k: v for k,v in corpus_dict.items() if string_clean in v}
        result = blltn[blltn.index.isin(list(fidnigns_dict))]     
        return list(result['Companyname'])
      
    



# key_words = keyword_dict


# blltn

def map_top_40_firms(df, keywrds, entity_mapper):
 
    top_40 = keywrds.parse('top_40_firms')   
    
    
    top_40 = top_40.rename ({"name":"raw"}, axis = 1)
    
    top_40['firm_n'] =  top_40['raw'].apply(lambda x : f_r.norm_firm_names(x))
    
    top_40['firm_n'] =  top_40['firm_n'].apply(lambda x : f_r.remove_orga_string(x))
    
    top_mapper = dict(zip(top_40['firm_n'], top_40['raw']))
    
    t = pd.DataFrame.from_dict(entity_mapper['corpus'], orient ='index')
    t[0] =  t[0].apply(lambda x : f_r.remove_orga_string(x))
    
    treshold = 0.80
    m = match_strings(top_40['firm_n'],  t[0], min_similarity = treshold)
      
    top_40_map  = dict(m.groupby('left_firm_n')['right_index'].apply(lambda x: list(np.unique(x))))
       
    all_entity_mapper = dict(entity_mapper['bulletin_entities'])
    all_entity_mapper.update(entity_mapper['insitutions_enties'])
    
    top_40_map  = {top_mapper[k] : [all_entity_mapper[x] for x in v ] for k,v in top_40_map.items()}
   
    return top_40_map
   



