# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 15:03:32 2022

@author: fs.egb
"""


import network
import owner


def get_og_network(df,base):
    """ 
    build a network of all owner until 1990 and group them by cluster
    
    """
    name_mapper = dict(zip(base['raw'], base['id']))
    
    df = owner.map_owner_ids(df, name_mapper)

    df = owner.map_all_owner_ids(df, firm_id = 'firm_id')

    og_mapper  = network.get_og_network(blltn = df ,
                                        og_year = 1990)
    
    base['og'] = base['id'].map(og_mapper)
    base['og'] = base['og'].fillna(base['id'])
    
    return base
