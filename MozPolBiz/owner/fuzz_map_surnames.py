# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 13:14:42 2022

@author: fs.egb
"""


import pandas as pd
from string_grouper import group_similar_strings


import owner


def fuzz_map_surnames(all_names, family_fuzz):
    """
    Fuzzy matches the last string of every name that is >4 strings.
    Returns base df with both direct names and fuzz matched names.

    Parameters
    ----------
    all_names : list
        List of names. Dropes everying >4 strings
    family_fuzz : integer
        treshold for fuzzy matching.

    Returns
    -------
    base : DataFrame
        raw names, with family names and fuzzy family names

    """
    try:
        family_fuzz
    except NameError:
        family_fuzz = 0.88
        print(f"define treshold family_fuzz as {family_fuzz}")


    all_names = [x for x in all_names if len(x)> 4]

    base = pd.DataFrame(all_names, columns = ['raw'])
    base['clean'] =  base['raw'].map(owner.clean_name_strings(all_names))
    surname_mapper = owner.get_surnames(base['clean'])
    base['family'] = base['clean'].map(surname_mapper)

    base['family_beta'] = group_similar_strings(base['family'],
                                          min_similarity = family_fuzz,
                                          )

    diff = len(base['family'].unique()) - len(base['family_beta'].unique())
    print(f" After fuzzy match {diff} fewer family names \n")
    return base
