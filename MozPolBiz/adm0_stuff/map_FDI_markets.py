# -*- coding: utf-8 -*-
"""
Created on Thu Sep  9 11:24:04 2021

@author: fs.egb


match FDI markets on bulletin entries
"""

from string_grouper import match_strings
import re as re
import pandas as pd 
# supress SettingWithCopyWarning:
pd.options.mode.chained_assignment = None  # default='warn'
import numpy as np
import adm0_stuff


def clean_FDI_intern(df, keyword_dict):
    df = df.dropna(subset = ['Investing company'])
    df = df.iloc[1:]
    df['y'] = df['Project date'].apply ( lambda x: x.year)
    print("String of Investing companies:")
    print(len(df['Investing company'].unique()))
    
    FDI_duplicates  = keyword_dict.parse('FDI_duplicates')
    FDI_duplicates = dict(zip(FDI_duplicates['Duplicate'], FDI_duplicates['unique']))
    FDI_duplicates = {k.strip(): v.strip() for k,v in FDI_duplicates.items()}
    
    df['IC'] =  df['Investing company'].map(FDI_duplicates)
    df['IC'] = df['IC'].fillna(df['Investing company'])
    print("String of unique names:")
    print(len(df['IC'].unique()))  
    df['IC'] = df['IC'].apply(lambda x : re.sub(r"\([^()]*\)", "", x))
    

    # replace IC string with original string if original mapped
    hand = keyword_dict.parse('FDI_firms')        
    keep_those = list(set(hand['FDI_Markets_names'])) 
       
    
    df.loc[df['Investing company'].isin(keep_those), 'IC'] = np.NAN
    df['IC'] = df['IC'].fillna(df['Investing company'])
    
  
    return df[['y', 'IC', 'Investing company']]
    
 
 
# def match_fdi_bulltn(fdi_df, blltn):
#     unique_FDI = pd.Series(fdi_df['IC'].unique().astype(str))
#     unique_blltn = pd.Series(blltn['Companyname'].astype(str))
#     m = match_strings(unique_FDI, unique_blltn, min_similarity = 0.80)
    
#     m_dict = dict(zip(m['right_ID do Registo'],m['left_side'])) 
    
    
#     blltn['FDI'] = blltn.index.map(m_dict)
#     return dict(zip(blltn.index, blltn['FDI']))
    



# df = bulletin.copy()

# fdi_markets = fdi_m.copy()

# key_words = keyword_dict
      
def map_FDI_markets(df,fdi_markets, key_words):   
    fdi_markets = fdi_markets[fdi_markets['Investing company']!= 'Investing company']
#   map FDI projects on bulletin raw firm  strings per hand:
    hand = key_words.parse('FDI_firms')        
    hand['FDI_Markets_names'] = hand['FDI_Markets_names'].str.strip()
    
    # first match the manuell matches on the bulletin
    manual_map = dict(zip(hand['bulletin_name'], hand['FDI_Markets_names']))
    df['FDI_project'] = df['Companyname'].map(manual_map)   
    del manual_map, hand
    
    print(len(df['FDI_project'].unique()), " manual matches FDI projects on raw bulletin string ")
   

 # clean FDI company names and fzzymatch on bulletin that have no FDI affiliation

    # df_no = df[df['FDI_project'].isna()]

    fdi_clean = clean_FDI_intern(fdi_markets, key_words)

    
    fdi_clean = adm0_stuff.process_firm_string(fdi_clean,'IC')
    
    m = match_strings(df['firm_n'],fdi_clean['firm_n'], min_similarity = 0.80)
   
    mm_mapper = dict(zip(m['left_firm_n'], m['right_firm_n']))
    
    # replace cleaned names with initical IC name
    
    # -> need to make sure that the IC and the hand matches are the same.
    
    temp = dict(zip(fdi_clean['firm_n'], fdi_clean['IC']))
    
    mm_mapper = {k: temp[v] for k,v in mm_mapper.items()}

    
    df['FDI_project_beta'] = df['firm_n'].map(mm_mapper)
    
    
    df['FDI_project'] = df['FDI_project'].fillna(df['FDI_project_beta'])
    
    df = df.drop(['FDI_project_beta'],1)
    
    mapped_FDIs = list(df['FDI_project'].unique())
    

   
    missing_FDIs = [x for x in list(fdi_clean['IC'].unique()) if x not in mapped_FDIs]
    
    # use orgininal string name
    temp = dict(zip(fdi_clean['IC'],fdi_clean['Investing company']))
    
    missing_FDIs = [temp[x] for x in missing_FDIs]
    
    print(len(missing_FDIs), " FDIs missing")
    
  
    return df, missing_FDIs
    
    
 ############# use these function to find unknown FDI projects ####################   
def creat_blltn_corpus(blltn):
    blltn = blltn [['Old name','Companyname', 'New name', 'Technical notes', 'Social object', 'Institutions partners']]
    blltn['all'] = blltn[blltn.columns].apply(lambda x: " ".join(x.dropna().astype(str)), axis=1)
    corpus_dict = dict(zip(blltn.index, blltn['all'] ))
    corpus_dict = {k: v.replace(",", " ") for k,v in corpus_dict.items()}  
    corpus_dict = {k: v.replace("-", " ") for k,v in corpus_dict.items()}  
    return {k: unidecode(v.lower()) for k,v in corpus_dict.items()}



def search_keywords_in_bulletin(x, corpus_dict, blltn):
        string_clean = unidecode(x.lower())
        fidnigns_dict =  {k: v for k,v in corpus_dict.items() if string_clean in v}
        result = blltn[blltn.index.isin(list(fidnigns_dict))]     
        for x in list(set(result['Companyname'])):
            print (x )
            
        result = result[['Companyname', 'New name', 'Technical notes', 'Social object', 'Date of writing', 
                          'Place of the seat','Institutions partners', 'FDI_project']]
  
        return result 




# corpus =  creat_blltn_corpus(bltn)   

#  x = 'Tripartida '
# findings = search_keywords_in_bulletin(x, corpus, bltn)
  
 
# xx = fdi_m[fdi_m['Investing company'].isin(missing_FDIs)]

# fdi_m['Investing company'] = fdi_m['Investing company'].fillna('')

# tes = bulletin[bulletin.index == 7201]
