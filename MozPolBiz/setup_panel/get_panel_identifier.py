# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 12:32:21 2022

@author: fs.egb
"""
import pandas as pd

def get_panel_identifier(y_i, all_owners):  
    product = []
    for ow in all_owners:
        product.extend( [(ow,y)  for y in list(y_i)])
    panel = pd.DataFrame(product, columns = ['id','y'])
                    
    panel["m"] = panel[["id","y"]].apply(tuple, axis=1)    
    return panel