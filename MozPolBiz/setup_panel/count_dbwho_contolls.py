# -*- coding: utf-8 -*-
"""
Created on Mon Sep  5 09:22:35 2022

@author: fs.egb
"""
import pandas as pd

import setup_panel

def count_dbwho_contolls(df,f_all, y_i):
    """ 
    ( Sam mail  9/2)
    3 ADDITIONAL VARIABLES IN THE OUTCOME_VARS FILES, 
    WHICH SEPARATELY COUNT THE NUMBER OF “associacao”, “fundacao” AND “pol_party” 
    IN WHICH THE INDIVIDUAL IS A NAMED PARTNER (SÓCIO). 
    SO, FOR PERSON i IN PERIOD t EACH VARIABLE WOULD 
    COUNT THE CUMULATIVE NUMBER OF ENTITIES OF A GIVEN 
    TYPE IN WHICH THE INDIVIDUAL IS A NAMED SÓCIO.          
    """
    frames = []
    for y in y_i:
        annula_reg = df[df['y']<= y]
        sub_p = f_all[f_all['y']== y]
        for orga in ['associacao','fundacao','partido politico']:
            temp = annula_reg[annula_reg['orga_type']== orga]
            all_entitiy_reg, firm_dict = setup_panel.get_owner_reg(temp)
            length =  {k: len(v) for k,v in  all_entitiy_reg.items()}
            sub_p[orga] = sub_p['id'].map(length)
            
        frames.append(sub_p)
           
    out_panel = pd.concat(frames)      
    # out_panel = out_panel.drop(columns = ['id','y'])
    
    return out_panel

