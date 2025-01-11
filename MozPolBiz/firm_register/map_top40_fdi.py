# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 15:31:36 2022

@author: fs.egb

link_institutions names across flexicadastre, fdi markets and 
"""

# from string_grouper import match_strings, group_similar_strings

# from pathlib import Path


import pandas as pd 


# supress SettingWithCopyWarning:
pd.options.mode.chained_assignment = None  # default='warn'
import numpy as np

import firm_register as f_r



# def load_data_for_now():
#     df = pd.read_pickle(r"C:\Users\fs.egb\Documents\moz\PoliConMz\pipeline\firmregister_temp.pkl")

#     d = Path.cwd().parent.parent/Path("data","fdi","FDImarkets_moz.xlsx")
    
#     fdi_markets = pd.ExcelFile(d).parse('fDiMarkets')
    
    
#     fdi_markets.columns = fdi_markets.iloc[1]
    
#     entity_mapper = {}
#     df, entity_mapper['bulletin_entities'] = f_r.define_entities(df)
    
#     df, entity_mapper  = f_r.process_institution_entities(df, entity_mapper)
    
#     keywrds= pd.ExcelFile(str(Path.cwd().parent/Path("data",
#             "all_keywords_mapper.xlsx"))) 
    
#     local_path = Path.cwd().parent/Path("data")
#     flexi = pd.read_pickle(local_path/Path("flexi","national_flexi_full.pkl"))

    
#     return df, fdi_markets, entity_mapper, keywrds, flexi


 
  
def find_entity(df, entity_mapper, search_term):    
  search_term = f_r.norm_firm_names(search_term)
  search_term = f_r.lemmatizing_entity_names(search_term)
  search_term = f_r.remove_orga_string(search_term)
  
  
  all_entity_mapper = entity_mapper['all_entity_mapper']

  corpus = entity_mapper['corpus']
  
  match = {k: v for k, v in corpus.items() if search_term in v}

  show = {k : all_entity_mapper[k] for k in match.keys() }       
  for k in list(show):

      print(f"{k}:{show[k]}")
      

  firms = [x for x in list(show.values()) if isinstance(x, int)]
  institutions = [x for x in list(show.values()) if not isinstance(x, int)]
  
  df_firms = df[df['entity_id'].isin(firms)]
  
  df['inst_owner_norm'] = df['inst_owner_norm'].fillna("")
  for i in institutions:
      df_institutions = df[df['inst_owner_norm'].str.contains(i)]
      df_firms =  df_firms.append(df_institutions)

  
  return df_firms
      
      
  
def map_top40_by_hand(entity_mapper, keywrds):
    df = keywrds.parse('top_40_manual_map')
    hand_map  = dict(df.groupby('top_40_name')['bulletin_name'].apply(lambda x: list(np.unique(x))))
    hand_map  = {k: [entity_mapper['all_entity_mapper'][x] for x in v] for k,v in hand_map.items()}
    return hand_map
  
    

          


def map_top40_fdi(df, fdi_markets, entity_mapper, keywrds, flexi):
    """ map fdi markets both on bulletin enttries aswell as flexi cadastre licenses """
    fdi_markets['Project date']= pd.to_datetime(fdi_markets['Project date'], 
                                                errors='coerce')
    
    
    fdi_markets = fdi_markets.dropna(subset=['Project date'])
    fdi_all_matches =  f_r.map_FDI_markets(df, fdi_markets,entity_mapper , keywrds, flexi)
    
    
    top_40_map =  f_r.map_top_40_firms(df, keywrds, entity_mapper)
    top_40_map.update(map_top40_by_hand(entity_mapper, keywrds))
    
    
   
    gas_shareholders = f_r.map_inp(fdi_markets['Investing company'],keywrds, entity_mapper)
    
    temp = gas_shareholders.copy()
    temp['FDI_link'] = temp['FDI_link'].fillna(temp['hand_match'])
    
    fdi_gas_mapper = dict(zip(temp['FDI_link'], temp ['affi_gas_fields']))
    fdi_gas_mapper = {k: v for k,v in fdi_gas_mapper.items() if k in list(fdi_markets['Investing company']) }
    
    fdi_all_matches.update(fdi_gas_mapper)
    
    entity_mapper['fdi_projects'] = dict(fdi_all_matches)
    
    
    entity_mapper['top40_firms'] = dict(top_40_map)
    
    return entity_mapper 


# df, fdi_markets, entity_mapper, keywrds, flexi = load_data_for_now()


# entity_mapper =  map_top40_fdi(df, fdi_markets, entity_mapper, keywrds, flexi)
    
    
    
# def fliex_owners():
  
#     unique_owners = {x: x for x in flexi['entity'].unique()}
#     unique_owners = {k: f_r.norm_firm_names(v) for k, v in unique_owners.items()}
#     unique_owners = {k: f_r.lemmatizing_entity_names(v) for k, v in unique_owners.items()}  
#     unique_owners = {k: f_r.remove_orga_string(v) for k, v in unique_owners.items()}  
    
#     treshold = 0.70
#     m = match_strings(pd.Series(unique_owners),  pd.Series(entity_mapper['corpus']),
#                       min_similarity = treshold)
#     fdi_flexi_map  = dict(zip( m['right_Investing company'], m['left_entity']))


    
    # for u in flexi['entity'].unique():
    #     temp = flexi['entity'][]
        
        
    #     flexi['string'] = institutions['string'].apply(lambda x:)
    
    




