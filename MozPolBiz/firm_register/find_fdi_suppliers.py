# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 09:00:39 2022

@author: fs.egb
"""



def find_fdi_suppliers(df):
    temp = df.copy()
    temp = temp[['firm_id','Companyname','Social object','firm_id_countes']]
    
    social_dict =  (dict(zip(temp.index, temp['Social object'])))
    
    company_name_dict =  (dict(zip(temp.index, temp['Companyname'])))
    
    
    
    
    
    
    