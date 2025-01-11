# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 10:23:25 2022

@author: fs.egb
"""



import sqlite3
# from tqdm import tqdm
import pandas as pd



def get_all_tables(local_path):
    with sqlite3.connect(local_path) as conn:
        command = """SELECT name FROM sqlite_master  
                    WHERE type='table';"""
        cursor = conn.execute(command)
        myresult = cursor.fetchall()
        names = set()
        for x in myresult:
            names.add(str(x))
            
    names = [x[2:4] for x in names if "flexicadastre" in x ]
    names = set(names)
    
    return names
    