# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 12:30:29 2022

@author: fs.egb

commodities
"""

import sqlite3
from tqdm import tqdm
import pandas as pd


def get_country_commodities(local_path, cntry_lower_2):
    """ 
    fetch df of commodities form sql table
    """
    print("fetches only the type of commity per feature id")
    output = []
    with sqlite3.connect(local_path) as conn:
        command = f"SELECT * FROM {cntry_lower_2}_flexicadastre_commodity"
        cursor = conn.execute(command)
        for row in cursor:
            output.append(row)
            
    # create DataFrame using data
    name_of_cols = list(map(lambda x: x[0], cursor.description))
        
    df = pd.DataFrame(output, columns = name_of_cols)
    return df


def get_commodities_per_feature(local_path, cntry_lower_2):
    """
    map all Commoditis uniuqe Feature IDs , i.e. licenses
    
    """
    df = get_country_commodities(local_path, cntry_lower_2)
    # map names on FeatureId
    out = {}
    for i in tqdm(df['FeatureId'].unique()):
        temp = df.loc[(df['FeatureId'] == i)]
        out[i] =', '.join(temp['Commodity'])
        
    return out
           
    
