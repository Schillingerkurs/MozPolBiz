# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 08:59:47 2021

@author: fs.egb


firm entities


"""

import pandas as pd
from unidecode import unidecode
from string_grouper import match_strings, group_similar_strings
import random


stop_words = ['limitada','sociedade unipessoal', "s.a.", 's. a.',
              's.a','lda','ltd', 'sa','sarl', 's.a.r.l.']

def normalize_firm_names(blltn,  stop_words , v_match):
    """ normalize firm names, remove stopwards and fuzzy map  """
    bl_dict = dict(zip(blltn, blltn))
    bl_dict = {k:  unidecode(str(v).lower()) for k,v in bl_dict.items()}
    bl_dict = {k:  v.strip() for k,v in bl_dict.items()}
    bl_dict = {k:  v.split(" ") for k,v in bl_dict.items()}
    for x in stop_words:
        bl_dict = {k: [x for x in v if x not in stop_words] for k, v in bl_dict.items()}
    bl_dict = {k: " ".join(v) for k, v in bl_dict.items()}
    bl_dict = {k: v.replace(",","") for k, v in bl_dict.items()}

    bl_names = pd.DataFrame.from_dict(bl_dict, orient= 'index')
    bl_names = bl_names.reset_index()
        # map intern
    bl_names['unique'] = group_similar_strings(bl_names[0], min_similarity = v_match)
    bl_names['dupl_firms' ] = bl_names['unique'].map(bl_names['unique'].value_counts())

    bl_mapper = dict (zip(bl_names['index'], bl_names['unique']))

    return {k : v.strip() for k, v in bl_mapper.items()}



def inst_partner_dict(df):
    #  seperate institutional partners
    inst_dict = dict(zip(df.index, df['Institutions partners']))
    inst_dict = {k: v for k,v in inst_dict.items() if str(v) != 'nan'}
    inst_dict = {k: v.split( "||") for k,v in inst_dict.items() }
    return {k: [x.replace("|", "") for x in v] for k,v in inst_dict.items() }


def inst_int_clean(dict_):
    inst_names = list(set([i for s in  list(dict_.values()) for i in s]))

    df_mapper = normalize_firm_names(inst_names, stop_words, 0.82)
    x = len(df_mapper) -  len(set(df_mapper.values()))
    print ( x ," duplicates within inst. partners found")

    dict_ = {k: [df_mapper[x] for x in v] for k,v in dict_.items()}
    # drop entries if only 3 strings
    dict_ = {k: [x for x in v  if len(x) > 3] for  k,v in dict_.items()}


    return {k: v for k,v in dict_.items() if v !=  []}


def process_firm_string(df,column):
    v_match = 0.85
    mapper = normalize_firm_names(df[column],  stop_words , v_match)
    df['firm_n'] = df[column].map(mapper)
    return df






def process_all_firm_strings(input_):

    inst_firms = inst_partner_dict(input_)

    inst_firms = inst_int_clean(inst_firms)


    all_names = list(set(input_['Companyname']))
    print(len(all_names)," unqiue names in company column")

    all_names.extend(list(set([i for s in  list(inst_firms.values()) for i in s])))
    print(len(all_names)," with institutional partners")


    df_mapper = normalize_firm_names(all_names, stop_words, 0.95)


    x = len(df_mapper) -  len(set(df_mapper.values()))
    print ( x ," firm name duplicates found")


    # map clean names on institutional dict and then the bulletin
    inst_firms = {k: [df_mapper[x] for x in v] for k,v in inst_firms.items()}

    len_ins = {k: len(v) for k,v in inst_firms.items()}


    input_['no_parents_all'] = input_.index.map(len_ins)

    input_['all_parent_firm'] = input_.index.map(inst_firms)


    input_['firm_n'] = input_['Companyname'].map(df_mapper)

    unique_bulletin_names = list(set(input_['firm_n']))


    domnestic_partents = {k: [x for x in v if x in unique_bulletin_names] for k,v in inst_firms.items()}
    domnestic_partents = {k: v for k,v in domnestic_partents.items() if v !=[]}
    len_dom_par =  {k: len(v) for k,v in domnestic_partents.items()}
    input_['no_dom_parents'] = input_.index.map(len_dom_par)


    return input_

    """  explore unknown institutional partners """
    # unknown_foreign_firms = {k: [x for x in v if x not in unique_bulletin_names] for k,v in inst_firms.items()}
    # unknown_foreign_firms = {k: v for k,v in unknown_foreign_firms.items() if v !=[]}
    # unknown_list = (list(set([i for s in  list(unknown_foreign_firms.values()) for i in s])))











# input_ = bulletin.copy()




