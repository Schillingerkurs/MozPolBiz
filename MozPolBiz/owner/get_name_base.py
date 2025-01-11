# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 11:41:21 2022

@author: fs.egb
"""
from pathlib import Path
import pandas as pd
import owner
from string_grouper import group_similar_strings




def get_name_base(all_names = list(), other = dict())-> pd.DataFrame():
    """ setup main characterisitcs of an individual """


    base = (
            owner
            .get_surname_base(all_names, family_fuzz = 0.96)
            .query("family!= ''")
            .drop(columns =['family'])
            .rename(columns = {'family_beta': "family"}))



    base, first_name_matches = owner.map_family_subsets(base, first_name_fuzz = 0.75)

    base['alpha_clean'] = base['alpha_clean'].fillna(base['clean'])

    base['beta_clean'] = group_similar_strings(base['alpha_clean'],
                                          min_similarity = 0.89,
                                          )




    family_dict = owner.get_surnames(set(base['beta_clean']))


    base = (
            base
            .drop(columns = ['family', 'alpha_clean'])
            .assign(family = lambda x : x['beta_clean'].map(family_dict))
            )





    # base = test_name_mapper.type_one_error_check(base, entry_names)
    base = owner.map_initials(base)
    base = owner.map_gender(base, other)
    id_mapper = owner.set_id(base['beta_clean'], "person_")
    base['id'] = base['beta_clean'].map(id_mapper)

    base = owner.set_lawyer_dummy(base,other)

    base = owner.get_missing_names(all_names, base)


    dupl_counter = base['id'].value_counts()


    base =  (
            base
            .assign(lawyer = lambda x: x['lawyer'].astype(str))
            .assign(dupl_counter = lambda x: x['id'].map(dupl_counter))
            )

    return base
