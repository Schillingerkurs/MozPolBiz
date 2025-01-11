# -*- coding: utf-8 -*-
"""
Created on Wed May 18 09:31:37 2022

@author: fs.egb
"""

import pandas as pd



def count_unique_projects(df):
    """ count how many """
    mz_link_id = {}
    for n,l in enumerate(df['mz_link'].unique()):
        mz_link_id[l] = n

    df['mz_link_id'] = df['mz_link'].map(mz_link_id)
    
    return df


def formate_fdi_market(fdi_markets, entity_mapper):
    fdi_markets['mz_link'] = fdi_markets['Investing company'].map(entity_mapper['fdi_projects'])
    fdi_markets = fdi_markets[~fdi_markets['Project date'].apply (lambda x: isinstance(x, str))]
    fdi_markets = fdi_markets.set_index ('#')
    fdi_markets['y'] = pd.DatetimeIndex(fdi_markets['Project date']).year
    
    fdi_markets['mz_link'] = fdi_markets['mz_link'].\
    apply (lambda x : ", ".join([str(u) for u in x]) if isinstance(x,list) else x)

    fdi_markets = count_unique_projects(fdi_markets)

    return fdi_markets