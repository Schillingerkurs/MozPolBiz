# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 10:13:03 2022

@author: fs.egb

Prepare secondary data

"""

from pathlib import Path
import random
import pandas as pd
import re
import json
import numpy as np
pd.options.mode.chained_assignment = None  # default='warn'
import pickle
from string_grouper import match_strings, group_similar_strings
from unidecode import unidecode
# from firm_register.noramlize_entity_names import norm_firm_names


def load_secodnary_sources():
    
    d = Path.cwd().parent/Path("data", "fdi")
    
    
    fdi = pd.ExcelFile(d/Path("FDImarkets_moz.xlsx")).parse('fDiMarkets') 
    fdi.columns = fdi.iloc[1]
    
    m_m = pd.ExcelFile(d/Path("manual_mappings.xlsx"))
    # kywrds = {}
    # for k in m_m.sheet_names:
    #     kywrds[k] = m_m.parse(k)
    
    return fdi, m_m
 
def clean_FDI_intern(df, keyword_dict):
    """look if there are duplicates in the raw FDI markets data."""
    df = df.dropna(subset = ['Investing company'])
    df = df.iloc[1:]
    df['y'] = df['Project date'].apply ( lambda x: x.year)
    print("String of Investing companies in FDImarkets sheet:")
    print(len(df['Investing company'].unique()))
    
    FDI_duplicates  = keyword_dict.parse('FDI_duplicates')
    FDI_duplicates = dict(zip(FDI_duplicates['Duplicate'], FDI_duplicates['unique']))
    FDI_duplicates = {k.strip(): v.strip() for k,v in FDI_duplicates.items()}
    
    df['IC'] =  df['Investing company'].map(FDI_duplicates)
    df['IC'] = df['IC'].fillna(df['Investing company'])
    df['IC'] = df['IC'].apply(lambda x : re.sub(r"\([^()]*\)", "", x))
    
    # replace IC string with original string if original mapped
    hand = keyword_dict.parse('FDI_firms')        
    keep_those = list(set(hand['FDI_Markets_names'])) 
       
    
    df.loc[df['Investing company'].isin(keep_those), 'IC'] = np.NAN
    df['IC'] = df['IC'].fillna(df['Investing company'])
    
    print("Unique strings:")
    print(len(df['IC'].unique()))  
  
    return df


     
def map_FDI_markets(df,fdi_m, kywrds):  
    """
    Map bulletin Company names on FDI market projects.

    """
    fdi_m = fdi_m[fdi_m['Investing company']!= 'Investing company']
#   map FDI projects on bulletin raw firm  strings per hand:
    hand = kywrds.parse('FDI_firms')        
    hand['FDI_Markets_names'] = hand['FDI_Markets_names'].str.strip()
    
    # first match the manuell matches on the bulletin
    manual_map = dict(zip(hand['bulletin_name'], hand['FDI_Markets_names']))
    df['FDI_project'] = df['Companyname'].map(manual_map)   
    del manual_map, hand
    
    print(len(df['FDI_project'].unique()), " manual matches FDI projects on raw bulletin string ")
   

    fdi_clean = clean_FDI_intern(fdi_m, kywrds)
    
    
    fdi_clean = fdi_clean[['y', 'IC', 'Investing company']]   

    
    fdi_clean['firm_n'] = fdi_clean['IC'].apply(lambda x : norm_firm_names(x))
    
    m = match_strings(df['norm_name'],fdi_clean['firm_n'], min_similarity = 0.80)
   
    mm_mapper = dict(zip(m['left_norm_name'], m['right_firm_n']))
    
    # replace cleaned names with initical IC name
    
    # -> need to make sure that the IC and the hand matches are the same.
    
    temp = dict(zip(fdi_clean['firm_n'], fdi_clean['IC']))
    
    mm_mapper = {k: temp[v] for k,v in mm_mapper.items()}

    
    df['FDI_project_beta'] = df['norm_name'].map(mm_mapper)
    
    
    df['FDI_project'] = df['FDI_project'].fillna(df['FDI_project_beta'])
    
    df = df.drop(['FDI_project_beta'],1)
    
    mapped_FDIs = list(df['FDI_project'].unique())
    
    missing_FDIs = [x for x in list(fdi_clean['IC'].unique()) if x not in mapped_FDIs]
    
    # use orgininal string name
    temp = dict(zip(fdi_clean['IC'],fdi_clean['Investing company']))
    
    missing_FDIs = [temp[x] for x in missing_FDIs]
    
    print(len(missing_FDIs), " FDIs missing")
    
  
    return df, missing_FDIs
    

def create_blltn_corpus(blltn):
    """ 
    Build corpus of  bulletin entries
    """
    blltn = blltn [['Old name(s)','Companyname', 'New name',
                    'Additional information', 'Social object', 'Institution owner']]
    blltn['all'] = blltn[blltn.columns].apply(lambda x: " ".join(x.dropna().astype(str)), axis=1)
    corpus_dict = dict(zip(blltn.index, blltn['all'] ))
    corpus_dict = {k: v.replace(",", " ") for k,v in corpus_dict.items()}  
    corpus_dict = {k: v.replace("-", " ") for k,v in corpus_dict.items()}  
    return {k: unidecode(v.lower()) for k,v in corpus_dict.items()}
 
 
def search_keywords_in_bulletin(x, corpus_dict, blltn):
    """
    Search bulletin corpus for keywords
    """

    string_clean = unidecode(x.lower())
    fidnigns_dict =  {k: v for k,v in corpus_dict.items() if string_clean in v}
    result = blltn[blltn.index.isin(list(fidnigns_dict))]     
    for x in list(set(result['Companyname'])):
        print (x )
        
    result = result[['Companyname', 'New name', 'Additional information', 'Social object', 'Date of writing', 
                      'Place of the seat','Institution owner', 'FDI_project']]
  
    return result    
 
    
def map_important_firms(bltn, key_wrds, fdi_m):
    bltn = df.copy()
    fdi_m, kywrds = load_secodnary_sources()

    bltn, missing_FDIs = map_FDI_markets(bltn, fdi_m, kywrds)   
    bltn = map_top_40(bltn, kywrds )
    
    return bltn

# corpus =  create_blltn_corpus(df)   

# x = 'Sturrock '
# findings = search_keywords_in_bulletin(x, corpus, bltn)
    

