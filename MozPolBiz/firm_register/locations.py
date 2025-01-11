# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 09:25:03 2022

@author: fs.egb


geocode locations of HQ.

from 1) 'Place of the seat'
     2) 'Place of signature' & 'Place and date of signature'
"""

import numpy as np
from pathlib import Path
import pickle

from collections import Counter
import json


import firm_register

def load_temp_file():
    lp =  Path.cwd().parent.parent/Path("pipeline")
    with open(lp/Path("firmregister_full.pkl"), 'rb') as f:
       df = pickle.load(f)
       
    geo_code_path = Path.cwd().parent.parent/Path("data","geo_locations",
                                           "moz_admbnd_json")
    adm_information = {}       
    with open(geo_code_path.parent/Path("municipios_mz.pickle"),"rb") as f:    
        adm_information['municipios'] = pickle.load(f)
    f = open (geo_code_path/Path("moz_admbnda_adm3_ine_20190607.json"), "r")
    adm_information['adm3'] = json.loads(f.read())
       
       

    return df, adm_information



def find_a_primary_location(df):
    df['Place of the seat'] = df['Place of the seat'].replace('', np.nan) 
    df['Place of signature'] = df['Place of signature'].replace('', np.nan) 
    
    dstr_seat = df['Place of the seat'].value_counts(dropna= False)
    
    missing_share = round(len(df[df['Place of the seat'].isna()])/ len(df), 4)
    print(f'{missing_share*100} % of the rows report no Place of seat')
    
    
    loc_backup = dict(zip(df.index, df['Place and date of signature']))
    loc_backup = {k: v.split(",")[0] for k,v in loc_backup.items() if isinstance(v,str)}
    loc_backup = {k: v.strip() for k,v in loc_backup.items()}
    
    
    df = df.reset_index()
    df['Place of signature'] = df['Place of signature'].fillna(df['ID do Registo'].map(loc_backup))
    df = df.set_index('ID do Registo')
    
    missing_share = round(len(df[df['Place of signature'].isna()])/ len(df), 4)
    print(f'{missing_share*100} % of the rows report no "Place of signature"')
    
    df['primary_location'] = df['Place of the seat']
    df['primary_location'] = df['primary_location'].fillna(df['Place of signature'] )
    missing_share = round(len(df[df['primary_location'].isna()])/ len(df), 4)
    df['primary_location']  =  df['primary_location'].replace('', np.nan) 
    
    print(f'{missing_share*100} % of the rows report no "primary_location" \
          \n i.e. neither  "Place of signature" nor Place of seat')
    
    # t = df['primary_location'].value_counts(dropna = False )
    return df 

def get_all_adm_names(adm3):
    """ get raw and normalized adm3 names from geojson"""
    adm_all_raw = {}
    for e in adm3['features']:
        adm_all_raw[e['properties']['ADM3_PT']] = \
             {e['properties']['ADM2_PT']: e['properties']['ADM1_PT'] }
      
              
    return adm_all_raw
    

def rename_colonial_city_names(string):
    colonial_mapper = {"porto amelia": "pemba",
                      "lourenco marques": "maputo"
                     }
    for n in colonial_mapper:
        string = string.replace(n, colonial_mapper[n])
    return string


def adm_level_dict(adm_information):
    """ list level type per string """
    muncpls, rest = zip(*adm_information.items())
    level = {k: "municiple" for k in muncpls}
    districts = set([list(x.keys())[0] for x in rest])   
    level.update({k: "district" for k in districts})          
    province = set([list(x.values())[0] for x in rest])
    level.update({k: "province" for k in province})
    return level 

 
def adm_name_mapper(adm_name_dict):
    adm1, adm2, adm3,adm_all = [],[],[],[]
    for k in adm_name_dict:
        adm1.extend(list(adm_name_dict[k].values()))
        adm2.extend(list(adm_name_dict[k].keys()))
        adm3.append(k)
    adm_all.extend(list(set(adm1)))
    adm_all.extend(list(set(adm2)))
    adm_all.extend(list(set(adm3)))
    
    adm_norm_mapper = {x:firm_register.norm_locations(x) for x in adm_all}
    
    return adm_norm_mapper


   
def controll_province_level(adm_name_dict,df, reveresd_adm_norm):
    
    """ 
    report adm level as district if HQ reported only on province level
    """
    
    
    prov = df[df['adm_level']=='province']

    sig_mapper = dict(zip(prov.index,prov['Place and date of signature']))
    sig_mapper = {k: v.split(", ")[0] for k,v in sig_mapper.items() if isinstance(v,str)}
    
    sig_mapper =  {k: firm_register.norm_locations(v) for k, v in sig_mapper.items()}
    sig_mapper =  {k: rename_colonial_city_names(v) for k, v in sig_mapper.items()}  
    
    provinces = set(prov['adm_location'])
    
    
    all_replacements = {}
    for c in provinces:
        useful = {k: v for k, v in adm_name_dict.items() if c in v.values()}
        dstr = set([list(k.keys())[0] for k in useful.values()])
        passt = set(useful.keys()).union(dstr)
        
        passt = [firm_register.norm_locations(x) for x in passt]
        
        replace = {k:v for k,v in sig_mapper.items() if v in passt}
        replace = {k: reveresd_adm_norm[v] for k,v in replace.items()}
        
        all_replacements.update(replace)
    
    df['adm_2'] = df.index.map(all_replacements)
    
    
    df['adm_2'] = df['adm_2'].fillna(df['adm_location'] )
    
    
    return df
    
 

def find_most_active_district(df, adm_name_dict):
    onyl_dstr =  df[df['adm_level'] == 'district']
    
    disrict_mapper = {}    
    for k in adm_name_dict:
        disrict_mapper.update(adm_name_dict[k])
      
    onyl_dstr['province'] =  onyl_dstr['adm_2'].map(disrict_mapper)
    most_common_dstr ={}
    for p in set(onyl_dstr['province']):
        province_df = onyl_dstr[onyl_dstr['province']==p]
        most_common_dstr[p] = list(province_df['adm_2'].mode())[0]
    return most_common_dstr
        


       
def map_anything_on_adm_names(df, adm_information):

    """ map all bulletin locations of exisitng adm strings """
    
 
    adm_name_dict =  get_all_adm_names(adm_information['adm3'])
    
    adm_norm_mapper = adm_name_mapper(adm_name_dict)
    
    reveresd_adm_norm = {v:k for k,v in adm_norm_mapper.items()}


    df = find_a_primary_location(df)
    
    
    typos = {"Maptuto":["Maput/o","Maputoss","Mpauto","Mputo"],
              "Ilha De Mocambique (Cidade)":["Ilha/de/Moçambique"]}
    
    for m in typos:
        for l in typos[m]:
            df['primary_location'] = df['primary_location'].replace(l,m)
            
    temp = df[~df['primary_location'].isna()]
    
    hq_dict = dict(zip(temp.index, temp['primary_location'])) 
    hq_dict =  {k: firm_register.norm_locations(v) for k, v in hq_dict.items()}
    hq_dict =  {k: rename_colonial_city_names(v) for k, v in hq_dict.items()}    
    
    # find  adm nmaes form geosjon in hq entries
    hq_adm_match = {k: v for k,v in hq_dict.items() if v in  list(adm_norm_mapper.values())}
    hq_adm_match = {k: reveresd_adm_norm[v] for k,v in hq_adm_match.items()}


    df['adm_location'] = df.index.map(hq_adm_match)
    
    
    level = adm_level_dict(adm_name_dict)
    

    df['adm_level'] = df['adm_location'].map(level)
    print(f"HQ reported on province level: {len(df[df['adm_level']=='province'])}")
    
    
    df = controll_province_level(adm_name_dict,df, reveresd_adm_norm)
    
    df['adm_level'] = df['adm_2'].map(level)
    print(f"HQ and signature reported on province level: {len(df[df['adm_level']=='province'])}")
    

    df.loc[df['adm_level']=='province','imputed_adm'] = 1
    
    
    
    muncpl_mapper = {k: list(v.keys())[0] for k,v in adm_name_dict.items()}
    df['adm_2'] = df['adm_2'].replace(muncpl_mapper)
    
    
    most_common_dstr = find_most_active_district(df, adm_name_dict) 

    df['adm_2'] = df['adm_2'].replace(most_common_dstr)
    
    df['adm_level'] = df['adm_2'].map(level)
    print(df['adm_level'].value_counts(dropna = False))
    
    

       
    return df




# df, adm_information = load_temp_file() 


# df = map_anything_on_adm_names(df, adm_information)





   
    





