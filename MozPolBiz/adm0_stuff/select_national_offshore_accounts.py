# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 17:45:01 2022

@author: fs.egb
"""
import pandas as pd
from pathlib import Path

# from geopy.geocoders import Nominatim
# import geopandas as gpd


def select_national_offshore_accounts(HERE, iso3_cntry):
        
    p = Path(HERE/Path("data","external", "pandora_papers")).glob('**/*')
    all_paths = [x for x in p if x.is_file()]    
    relevant_files = {}
    for f in all_paths:
        file = pd.read_csv(f, low_memory=False)
        if "country_codes" in list(file.keys()):
            relevant_files[f.stem] = file.loc[file["country_codes"] == iso3_cntry]
            
    return relevant_files
   


# TODO: fiddle geolocations to the right spots     
# relevant_files = select_national_offshore_accounts(HERE, iso3_cntry)  

     
# node_adresses = {}
     
# for f in relevant_files:
#     if "address" in list(relevant_files[f].keys()):
#         temp = dict(zip(relevant_files[f]['node_id'], relevant_files[f]['address']))
#         node_adresses.update(temp)


# geolocator = Nominatim(user_agent="hunterxhunter")


# node_adresses = pd.DataFrame.from_dict(node_adresses, orient='index')



# adresses_locations = gpd.tools.geocode(node_adresses[0])
