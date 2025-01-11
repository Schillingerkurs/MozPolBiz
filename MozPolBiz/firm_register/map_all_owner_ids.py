# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 14:46:27 2022

@author: fs.egb
"""


def map_all_owner_ids(df,id_ ):
    """
    Map all owner ids on single firm ids. 
    ----------
    df : DataFrame
        bulletin
    id_ : string
        the ID columne of choirce.

    Returns
    -------
    df : DataFrame
        including all owner ids.

    """
    df['all_owner_ids'] = df[id_].map(df.groupby(id_)['owner_ids'].apply(list))
    df['all_owner_ids'] = df['all_owner_ids'].apply(lambda x : [i for s in x for i in s])
    df['all_owner_ids'] = df['all_owner_ids'].apply(lambda x : list(set(x)))
    df['all_owner_ids'] = df['all_owner_ids'].apply(lambda x: ", ".join(x))    
    
    df['firm_id_countes'] = df[id_].map(df[id_].value_counts())
    
    return df