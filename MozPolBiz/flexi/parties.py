# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 11:53:13 2022

@author: fs.egb

select party form national flexi
"""
import sqlite3
from tqdm import tqdm
import pandas as pd


def get_party_names(local_path, cntry_lower_2):
    print("fetch only the party name of each feature owning entity \n")
    output = []
    with sqlite3.connect(local_path) as conn:
        command = f"SELECT * FROM {cntry_lower_2}_flexicadastre_party"
        cursor = conn.execute(command)
        for row in cursor:
            output.append(row)
            
    name_of_cols = list(map(lambda x: x[0], cursor.description))
        
    df = pd.DataFrame(output, columns = name_of_cols)
 
    all_out = {}
    field_types = df['Field'].unique()
    
    print(f"{cntry_lower_2} has {len(field_types)} field types")
    
    for f in field_types:
        temp1 = df[df['Field'] == f]
        
        # map names on FeatureId
        out = {}
        for i in tqdm(temp1['FeatureId'].unique()):
            temp2 = temp1.loc[(temp1['FeatureId'] == i)]
            out[i] =', '.join(temp2['Party'])
        
        all_out[f] = out
    return all_out






