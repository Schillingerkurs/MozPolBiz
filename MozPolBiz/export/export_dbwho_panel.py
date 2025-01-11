# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 15:54:25 2022

@author: fs.egb
"""


from pathlib import Path
# import random
import pandas as pd
# import json
pd.options.mode.chained_assignment = None  # default='warn'




# own modules




def export_DBWHO_treatments(full_panel, filename, HERE):
    
    
    # full_panel['y'] = full_panel['y'].apply (lambda x : int(x)- 4)
    
    print("\n y variable changed to DBWHO labels")
    
    export_path = HERE/Path("data","processed")
     
    
    d = HERE/Path("data","raw",
                               "stata_export","description_vars.xlsx")


    trea_desc = pd.ExcelFile(d).parse("treatment")
    trea_desc = dict(zip (trea_desc['var'],trea_desc['description'] ))
    
    
    # there is also name_mapper
    print(f"Export STATA file direct into the DBWHO directory, i.e. {export_path}")
    
     
    full_panel.to_stata(export_path/Path(f"{filename}.dta"), 
                    version=117, 
                    variable_labels = trea_desc)
    
    



def export_DBWHO_outcomes(full_panel, filename, HERE):
    full_panel['y'] = full_panel['y'].apply (lambda x : int(x)- 4)

    print("\n y variable changed to DBWHO labels")
    
    export_path = HERE/Path("data","processed")
    
    d = HERE/Path("data","raw", "stata_export","description_vars.xlsx")

    trea_desc = pd.ExcelFile(d).parse("outcome")
    trea_desc = dict(zip (trea_desc['var'],trea_desc['description'] ))
       
    print(f"Export STATA file direct into the DBWHO directory, i.e. {export_path}")
    

    full_panel.to_stata(export_path/Path(f"{filename}.dta"), 
                    version=117) 
    
    
                    # variable_labels = trea_desc)
    

    
    
    
    
    
    
    




