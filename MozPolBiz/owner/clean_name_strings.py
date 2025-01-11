# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 16:05:28 2022

@author: fs.egb

map owner
"""


import pandas as pd
from unidecode import unidecode
import re


def get_unique_pep_names(pep_mandates):
    dict_ = dict(pep_mandates)
    t = pd.Series(dtype = str)
    for x in list(dict_):
        t = t.append(dict_[x]['name'])
    print(len(t), "unique PEP mandates \n")
    
    unique = list(set(list(t.astype(str))))
    print(len(unique), "unique raw PEP names \n")
        
    return unique

def clean_name_strings(all_names):
    dict_ = dict(zip(all_names,all_names))
    
    # # # # cleaning 
    
    dict_= {k:  re.sub(r"\([^()]*\)", "", v) for k, v in dict_.items()}   
    dict_= {k:  unidecode(v.lower()) for k, v in dict_.items()}   
    for x in ['"',"'", "%", "&", "#", "!", "]", "[",".","`","~", "80 mzn","|"]:
         dict_= {k:  v.replace(x,'') for k, v in dict_.items()}
         
    dict_= {k:  v.strip() for k, v in dict_.items()}
    dict_= {k:  v.replace("  "," ") for k, v in dict_.items()} 
    dict_= {k:  v.replace(" - "," ") for k, v in dict_.items()} 
    
    dict_= {k:  v for k, v in dict_.items() if  v[:2] !='- ' }      
    dict_= {k:  v[5:] if  v[:5] =='+ris ' else v  for k, v in dict_.items() }
    dict_= {k:  v[5:] if  v[:5] =='+lia ' else v  for k, v in dict_.items() }
    return dict_    
    



 
    