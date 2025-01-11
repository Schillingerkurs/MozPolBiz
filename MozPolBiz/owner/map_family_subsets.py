# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 17:17:49 2022

@author: fs.egb
"""

import pandas as pd
from string_grouper import group_similar_strings
from collections import Counter
from tqdm import tqdm


# import owner


def fuzzy_match_first_names(family_dict,
                         first_name_fuzz):
    """ fuzzy matches all first names in a family """
    unique_names = list(family_dict.values())
    unique_names = [item for t in unique_names for item in t]
    first_name_matches = {}
    if len(max(unique_names, key=len)) > 3:
        fuzzy = pd.DataFrame(set(unique_names), columns = ['raw'])

        fuzzy['fuzz'] = group_similar_strings(fuzzy['raw'],
                                              min_similarity = first_name_fuzz,
                                              )
        fuzzy = fuzzy[fuzzy['raw'] != fuzzy['fuzz']]
        mapper = dict(zip(fuzzy['raw'], fuzzy['fuzz']))
        if mapper != {}:
            first_name_matches.update(mapper)
            for name in family_dict:
                family_dict[name] = [mapper[x] if x in mapper else x for x in family_dict[name]]

    return family_dict, first_name_matches



def count_unique_names(base):
    out = {}
    for c in base.columns:
        out[c] = len(base[c].unique())
    print(out)
    return out



def map_family_subsets(base, first_name_fuzz):
    """
    Fuzzy match first names within a family.
    Find names that are fully subsets of other names.
    Map subsets on long names

    ----------
    base: DataFrame
        df with raw names aswell as family names

    first_name_fuzz: treshold for fuzzymatching of first names.

    Returns
    -------
    base : pd.DataFrame
        mapping if name is a perfect subset of .


    first_name_matches: dict
        matches from the first name matche per family.

    """
    surname_mapper = dict(zip(base['clean'], base['family']))

    surname_mapper_multi  = {k:v for k,v in Counter(surname_mapper.values()).items() if
                      v > 1}

    surname_mapper_multi= {k: v for k,v in
                    surname_mapper.items() if v in surname_mapper_multi}


    print("Create a dict for each family name")
    family_dict_raw  = {}
    for f in tqdm(surname_mapper_multi.values()):
        family_dict_raw[f] = [k for k, v in surname_mapper_multi.items() if v == f]

    family_dict_multi = {k: [x.replace(k,"") for x in v] for k,v in
                   family_dict_raw.items() }

    family_dict_multi = {k: [x.strip() for x in v if x != ''] for k,v in
                   family_dict_multi.items()}

    family_duplicates = {}

    print("\n Compare names within each family: \n ")
    all_first_name_matches = {}
    for f in tqdm(family_dict_multi):
        family_dict = {x: x.split(" ") for x in family_dict_multi[f]}
        family_dict, first_name_matches =  fuzzy_match_first_names(family_dict, first_name_fuzz)
        all_first_name_matches.update(first_name_matches)
        family_first_names = dict(family_dict)

        for name in family_first_names:
            if "junior" in name:
                family_first_names[name] = 'junior'
            if len(family_first_names[name]) > 1:
                family_first_names[name] = family_first_names[name][0]

            if len(family_first_names[name]) == 1:
                family_first_names[name] = "".join(family_first_names[name])

        for first_name in set(family_first_names.values()):
            pot_match = {k: v for k,v in family_first_names.items() if v == first_name}
            names = list(pot_match)
            longest_name = max(names, key=len)
            for n  in [x for x in names  if x != longest_name]:
                if n in longest_name:
                     family_duplicates[f'{n} {f}'] = f'{longest_name} {f}'

    base['alpha_clean'] = base['clean'].map(family_duplicates)

    return base, all_first_name_matches


