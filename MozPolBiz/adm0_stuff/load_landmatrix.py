# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 19:08:26 2022

@author: fs.egb
"""
import pandas as pd
from pathlib import Path

import geopandas as gpd

def load_landmatrix(HERE):  
    csv_files = [x for x in Path(HERE/Path("data","external", 
               "land_matrix")).glob('**/*') if ".csv" in str(x)]
    
    
    geo_file = [x for x in Path(HERE/Path("data","external", 
           "land_matrix")).glob('**/*') if ".geojson" in str(x)]
    
    
    all_tables = {}
    for a in csv_files:
         all_tables[a.stem] = (
             pd.read_csv(a, low_memory=False,
                     on_bad_lines='skip', sep = ";")
            .dropna(axis=1, how='all')
            )
                         
    
    geo = gpd.read_file(geo_file[0])


       
    out = {}
    frame = pd.DataFrame(set(geo['deal_id'])).set_index(0)  
    for k in all_tables.keys():
        if "Deal ID" in all_tables[k].keys():  
            temp = (all_tables[k]
                    .set_index("Deal ID")
                    .dropna(how='all', axis=1)
                    )
            frame = frame.merge(temp, left_index = True, right_index = True)
        else: 
            out[k] = all_tables[k]
                
             
    geo = geo.set_index("deal_id")  
    out['moz_deals'] = frame.merge(geo, left_index = True, 
                right_index = True)
    
    
    return out
    
    
    


