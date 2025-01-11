# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 10:07:16 2022

@author: fs.egb

flexi
"""
import pickle
import sqlite3
from pathlib import Path

# from tqdm import tqdm
import pandas as pd

HERE = Path(__file__).parent

col_n_mapper = {
    "DteGranted": "Grant_Date", 
    "DteStart":"Grant_Date"
    }


def load_flexi(db_path: str, cntry_lower_2: str) -> pd.DataFrame:
    """
    loads all entries from the national flexi table as a df 
    """
    output = []


    with sqlite3.connect(db_path) as conn:
        command = f"SELECT * FROM {cntry_lower_2}_flexicadastre"

        cursor = conn.execute(command)
        for row in cursor:
            output.append(row)
    names = list(map(lambda x: x[0], cursor.description))  
    df = pd.DataFrame(output, columns = names)
    col_n_mapper = {"DteGranted":"Grant_Date",
                    "DteStart":"Grant_Date",
                    "Expiry_Date":"Expiry_Dat",
                    'DteExpires': "Expiry_Dat",
                    'Application_Date':'DteApplied',
                    'Licence_Type':'Type',
                    'DteEnd':"Expiry_Dat",
                    'Sign_Date':'DteApplied'}
    
    df = df.rename(columns = col_n_mapper)

    if "Grant_Date" not in df.keys():
        raise ValueError(f"Need to update column name mapper for \n  \
              {cntry_lower_2} \n (Flexi name not consistent \n")

    if "Expiry_Dat" not in df.keys():
        raise ValueError(f"Need to update column name mapper for \n  \
              {cntry_lower_2} \n No column called 'Expiry_Dat'\n")
              
    def sjoin(x): return ';'.join(x[x.notnull()].astype(str))
    
    if len(set(df.keys())) != len(df.keys()):
        print("duplicate!")
        df = df.groupby(level=0, axis=1).apply(lambda x: x.apply(sjoin, axis=1))

    

    with sqlite3.connect(db_path) as conn:
        query = f"SELECT * FROM {cntry_lower_2}_flexicadastre"
        df = pd.read_sql_query(query, conn)

    if "Grant_Date" not in df.keys():
        df = df.rename(columns = col_n_mapper)
        if "Grant_Date" not in df.keys():
            print(f"Need to update column name mapper for \n",
                  "{cntry_lower_2} (Flexi name not consistent")

    return df





def load_mine_grid() ->  pd.DataFrame:

    fp = HERE.parent.parent / 'pipeline' / 'geospatial' / 't_m_i_m_baseline.pkl'
    with open(fp, 'rb') as f:
        df = pickle.load(f)
    return df
    
    


        
        
       
       
        
    