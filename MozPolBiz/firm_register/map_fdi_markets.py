# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 19:34:23 2022

@author: fs.egb

map FDI_Porjects
"""

from string_grouper import match_strings, group_similar_strings
import re as re
import pandas as pd
# supress SettingWithCopyWarning:
pd.options.mode.chained_assignment = None  # default='warn'
import numpy as np
import firm_register as f_r

from unidecode import unidecode



def map_fdi_m_on_bltn_entitis(mapper_dict,fdi_mapper):

    institutions =   pd.DataFrame.from_dict(mapper_dict , orient = 'index')
    institutions = institutions.reset_index().set_index(0)
    institutions.columns = ['string']
    institutions['string'] = institutions['string'].apply(lambda x: f_r.norm_firm_names(x))

    treshold = 0.75

    m = match_strings(fdi_mapper[0],  institutions['string'], min_similarity = treshold)

    fdi_entities_map  = dict(m.groupby('left_index')['right_0'].apply(lambda x: list(np.unique(x))))

    return fdi_entities_map


def fdi_m_handmatch(entity_mapper, keywrds):
    """ maps by hand from excel sheet """

    temp = dict(entity_mapper)

    hand = keywrds.parse('FDI_firms')
    hand['FDI_Markets_names'] = hand['FDI_Markets_names'].str.strip()

    hand['bulletin_name'] = hand['bulletin_name'].astype(str)

    hand_map  = dict(hand.groupby('FDI_Markets_names')['bulletin_name'].apply(lambda x: list(np.unique(x))))

    hand_map  = {k: [temp['all_entity_mapper'][x]
                     if x in temp['all_entity_mapper']  else x for x in v ]
                     for k,v in hand_map.items()}


    return  hand_map

def update_fdi_m_match(old_dict, new_dict):
    for f in old_dict:
         if f in list(new_dict):
             old_dict[f].extend(new_dict[f])
    for f in new_dict:
        if f not in old_dict.keys():
            old_dict[f] = new_dict[f]
    return old_dict



def handle_flexi(flexi, fdi_markets):


    # flexi_concessions  = dict(zip(flexi['parties'],flexi['code']))
    # flexi_concessions  = {k:v for k,v in flexi_concessions.items() if v is not None}
    treshold = 0.65

    flexi['parties'] = flexi['parties'].apply(lambda x: unidecode(str(x)))
    fdi_markets['Investing company'] = fdi_markets['Investing company'].apply(lambda x: unidecode(str(x)))
    m = match_strings(flexi['parties'],  fdi_markets['Investing company'], min_similarity = treshold)
    fdi_flexi_map  = dict(zip( m['right_Investing company'], m['left_parties']))

    return fdi_flexi_map





def map_FDI_markets(df,fdi_markets,entity_mapper, keywrds, flexi):

    temp = dict(entity_mapper)
    print("Sunshine, sunshine reggae")


    unique_fdi_pros = [str(x) for x in fdi_markets['Investing company'].unique()]

    unique_fdi_pros =  {k: f_r.norm_firm_names(k) for k  in unique_fdi_pros}
    unique_fdi_pros =  {k: f_r.lemmatizing_entity_names(v) for k,v in unique_fdi_pros.items()}
    unique_fdi_pros =  {k: f_r.remove_orga_string(v) for k,v in unique_fdi_pros.items()}
    unique_fdi_pros =  {str(k): str(v) for k,v in  unique_fdi_pros.items()}



    treshold = 0.85


    fdi_mapper = pd.DataFrame.from_dict(unique_fdi_pros,
                                       orient = 'index')



    fdi_mapper[0] = fdi_mapper[0].apply(lambda x: str(x) if not isinstance(x, str) else x)



    fdi_mapper[0] = group_similar_strings(fdi_mapper[0],
                                                  min_similarity = treshold
                                                  )

    fdi_instituions = map_fdi_m_on_bltn_entitis(temp['insitutions_enties'], fdi_mapper)
    fdi_blltn_firms = map_fdi_m_on_bltn_entitis(temp['bulletin_entities'], fdi_mapper)


    fdi_all_matches = update_fdi_m_match(fdi_instituions, fdi_blltn_firms)


    hand_mappings = fdi_m_handmatch(temp, keywrds)


    fdi_all_matches = update_fdi_m_match(fdi_all_matches, hand_mappings)


    flexi_match =  handle_flexi(flexi, fdi_markets)
    flexi_match = {k: v.split(", ") for k,v in flexi_match.items()}


    fdi_all_matches = update_fdi_m_match(fdi_all_matches, flexi_match)



    return fdi_all_matches


def get_descriptuves_of_fdi_markets(fdi_markets):

    fdi_markets['Project date']= pd.to_datetime(fdi_markets['Project date'],
                                            errors='coerce')

    fdi_markets = fdi_markets.dropna(subset=['Project date'])

    unique = len(fdi_markets['Investing company'].unique())

    first_y =  fdi_markets['Project date'].min()
    last_y =  fdi_markets['Project date'].max()

    print("Unique projects:", unique, "between", first_y, "\n and",last_y)

    sectors = fdi_markets['Sector'].value_counts()
    orgin_countries = fdi_markets['Source country'].value_counts()


    sectors = sectors.to_latex()

    print(sectors)

    return















