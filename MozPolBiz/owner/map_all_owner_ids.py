# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 11:46:08 2022

@author: fs.egb
"""

def map_all_owner_ids(df,firm_id):
    """
    Map all owner ids on single firm ids. 
    ----------
    df : DataFrame
        bulletin
    firm_id : string
        the ID columne of choirce.

    Returns
    -------
    df : DataFrame
        including all owner ids.

    """
    df['all_owner_ids'] = df[firm_id].map(df.groupby(firm_id)['owner_ids'].apply(list))
    df['all_owner_ids'] = df['all_owner_ids'].apply(lambda x : [i for s in x for i in s])
    df['all_owner_ids'] = df['all_owner_ids'].apply(lambda x : list(set(x)))
    df['all_owner_ids'] = df['all_owner_ids'].apply(lambda x: ", ".join(x))    
    
    df['firm_id_countes'] = df[firm_id].map(df[firm_id].value_counts())
    
    return df
