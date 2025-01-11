# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 12:16:15 2022

@author: fs.egb
"""


import pandas as pd
from string_grouper import group_similar_strings
from collections import defaultdict

import owner

def map_name_list(all_names, treshold):


    out_df_ = pd.DataFrame(all_names, columns =['raw'] )
    out_df_['clean'] = out_df_['raw'].map(owner.clean_name_strings(all_names))
    out_df_['clean'] = out_df_['clean'].fillna('')
    out_df_['unique'] = group_similar_strings(out_df_['clean'], \
                          min_similarity = treshold)
    name_mapper = dict(zip(out_df_['raw'],out_df_['unique']))

    print(len(name_mapper.keys()), "unique raw names \n")
    print(len(set(name_mapper.values())), " unique matched names \n")

    res = defaultdict(list)
    for key, val in sorted(name_mapper.items()):
        res[val].append(key)

    matches = {k: v for k,v in  res.items() if len(v) >1 }
    return name_mapper, matches


