# -*- coding: utf-8 -*-
"""
Created on Fri Feb 25 12:13:32 2022

@author: fs.egb

match old names, current names and new name of entities in to a unfiorm format

"""
from unidecode import unidecode
import re
# import pandas as pd
from string_grouper import group_similar_strings


def get_kywords():
    kywords = ['s.a.r.l.','s. a. r. l.', "lda", "s.a.", "sociedade",
               "unipessoal",'ltd', " holdings"]
    return kywords

def lemmatizing_entity_names(s):
    """ remove comma between entity name and orgatype """
    kywords = get_kywords()
    for k in kywords:
        s = s.replace(f", {k}",f" {k}")
    s = s.strip(",")
    s = s.strip()

    return s

def remove_orga_string(s):
    """ remove all orga type info from string"""
    kywords = get_kywords()
    for k in kywords:
        s = s.replace(f"{k}","")
    s = s.strip()
    s = s.strip(",")
    s = s.strip()

    return s



def identify_firm_entities(name_list):
    """
    Identif limitada, unipersonal etc. in entity string
    Takes list, returns dict
    """
    kywords = get_kywords()
    out = {}
    for e in name_list:
        for word in kywords:
             if f" {word}" in e:
                out[e] = word

    return out



def norm_firm_names(s):
    s = unidecode(s.lower())
    s = s.replace(" sarl"," s. a. r. l.")
    s = s.replace(" s. a. r. l "," s. a. r. l.")
    s = s.replace(",limitada",", limitada")
    s = s.replace(" limitada"," lda")
    s = s.replace(" limited"," lda")
    s = s.replace(" lda."," lda")
    s = s.replace(",lda"," lda")
    s = s.replace(" sa "," s.a.")
    s = s.replace(" sa\b"," s.a.")
    s = s.replace(" s.a"," s.a.")
    s = s.replace(" s.a\b"," s.a.")
    s = s.replace(" s.a.."," s.a.")
    s = unidecode(re.sub(r'\([^)]*\)', '', s))
    s = s.replace("  "," ")
    s = s.strip()
    return s

def fuzzy_entity_norm(input_series):
    """ fuzzy match of entity string """
    treshold = 0.95

    df = input_series.to_frame()
    df.columns = ['input']
    print(f"\n cosine similarity fuzzy match: {treshold}")
    df['fuzzy'] = group_similar_strings(df['input'] , min_similarity = treshold
                                        )

    mapper = dict(zip(df['input'], df['fuzzy']))
    difference = len(df['input'].unique()) - len(df['fuzzy'].unique())
    print(f"\n {difference} fuzzy matches")
    return mapper



def norm_all_names(df):
    """
    Normalize all name columns and map current on old names,
    aswell as new names on current names
    ----------
    df : pd.DataFrame
        bulletin data from.

    Returns
    -------
    df : pd.Dataframe
        bulletin with normalized name entitiy.
    """
    m_m = df [['Companyname', 'Old name(s)', 'New name']]
    new_map = dict(zip(df['Companyname'], df['New name']))
    new_map = {k: norm_firm_names(v) for k, v in new_map.items() if isinstance(v,str)}
    m_m['norm'] = m_m['Companyname'].apply(lambda x: norm_firm_names(x))
    m_m['new_norm'] = m_m['Companyname'].map(new_map)

    m_m['new_norm'] = m_m['new_norm'].fillna(m_m['norm'])
    old_mapper = dict(zip(m_m['Old name(s)'],m_m['new_norm']))
    old_mapper = {norm_firm_names(k): v for k,v in old_mapper.items() if isinstance(k,str)}

    m_m['norm_gold'] = m_m['new_norm'].map(old_mapper)
    m_m['norm_gold'] = m_m['norm_gold'].fillna(m_m['new_norm'])
    compare = m_m.describe().T
    print (compare)
    gold_mapper = dict(zip(m_m.index, m_m['norm_gold']))
    df['norm_name'] = df.index.map(gold_mapper)

    return df

